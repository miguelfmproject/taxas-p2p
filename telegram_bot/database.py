import os

import psycopg

import json
from psycopg.types.json import Jsonb


def obter_conexao():
    """
    Abre uma conexão com o PostgreSQL configurado no Railway.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "A variável DATABASE_URL não está configurada."
        )

    return psycopg.connect(
        database_url,
        connect_timeout=10
    )


def testar_conexao():
    """
    Testa a conexão com o PostgreSQL.
    Retorna True se estiver funcionando.
    """
    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT 1")
            resultado = cursor.fetchone()

    return resultado == (1,)
  
######EXECUÇÃO DA INTEGRAÇÃO DAS TABELAS######

def criar_estrutura_banco():
    """
    Executa o schema.sql e cria as tabelas do RemitFlow.
    """
    from pathlib import Path

    caminho_schema = Path(__file__).with_name("schema.sql")

    if not caminho_schema.exists():
        raise FileNotFoundError(
            f"Arquivo SQL não encontrado: {caminho_schema}"
        )

    sql = caminho_schema.read_text(encoding="utf-8")

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)

    return True
    
#####CADASTRO DE CLIENTES#####

def salvar_cliente(
    telegram_user_id,
    username=None,
    first_name=None,
    last_name=None,
    phone=None
):
    """
    Cadastra um cliente ou atualiza seus dados existentes.
    Retorna o ID interno do cliente no PostgreSQL.
    """

    sql = """
        INSERT INTO customers (
            telegram_user_id,
            username,
            first_name,
            last_name,
            phone
        )
        VALUES (%s, %s, %s, %s, %s)

        ON CONFLICT (telegram_user_id)
        DO UPDATE SET
            username = COALESCE(EXCLUDED.username, customers.username),
            first_name = COALESCE(EXCLUDED.first_name, customers.first_name),
            last_name = COALESCE(EXCLUDED.last_name, customers.last_name),
            phone = COALESCE(EXCLUDED.phone, customers.phone),
            updated_at = NOW()

        RETURNING id;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    telegram_user_id,
                    username,
                    first_name,
                    last_name,
                    phone
                )
            )

            resultado = cursor.fetchone()

    return resultado[0]
    
#####REGISTRO E MANUTENÇÃO DE CONVERSAS#####

def obter_ou_criar_conversa(customer_id, chat_id):
    """
    Localiza uma conversa existente ou cria uma nova.
    Retorna o ID interno da conversa no PostgreSQL.
    """

    sql = """
        INSERT INTO conversations (
            customer_id,
            chat_id
        )
        VALUES (%s, %s)

        ON CONFLICT (chat_id)
        DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            updated_at = NOW()

        RETURNING id;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    customer_id,
                    chat_id
                )
            )

            resultado = cursor.fetchone()

    return resultado[0]


def salvar_mensagem(
    conversation_id,
    telegram_message_id=None,
    direction="incoming",
    message_type="text",
    content=None,
    file_id=None
):
    """
    Registra uma mensagem no histórico da conversa.
    Retorna o ID interno da mensagem no PostgreSQL.
    """

    sql = """
        INSERT INTO messages (
            conversation_id,
            telegram_message_id,
            direction,
            message_type,
            content,
            file_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    conversation_id,
                    telegram_message_id,
                    direction,
                    message_type,
                    content,
                    file_id
                )
            )

            resultado = cursor.fetchone()

    return resultado[0]


def obter_conversa_por_chat_id(chat_id):
    """
    Localiza o ID interno da conversa pelo chat_id do Telegram.
    Retorna None se a conversa ainda não existir.
    """

    sql = """
        SELECT id
        FROM conversations
        WHERE chat_id = %s;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (chat_id,)
            )

            resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    return None
    

##### REGISTRO DE COTAÇÕES #####

def salvar_cotacao(
    conversation_id,
    calculator_type,
    input_amount,
    result_data,
    rate_snapshot
):
    """
    Registra uma cotação no PostgreSQL.
    Preserva o resultado e as taxas utilizadas naquele momento.
    Retorna o ID interno da cotação.
    """

    resultado_json = Jsonb(
        json.loads(
            json.dumps(result_data, default=str)
        )
    )

    taxas_json = Jsonb(
        json.loads(
            json.dumps(rate_snapshot, default=str)
        )
    )

    sql = """
        INSERT INTO quotes (
            conversation_id,
            calculator_type,
            input_amount,
            result_data,
            rate_snapshot
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    conversation_id,
                    calculator_type,
                    input_amount,
                    resultado_json,
                    taxas_json
                )
            )

            resultado = cursor.fetchone()

    return resultado[0]


##### REGISTRO DE OPERAÇÕES #####

def criar_operacao(conversation_id):
    """
    Cria uma nova operação de remessa vinculada a uma conversa.
    Retorna o ID interno da operação no PostgreSQL.
    """

    sql = """
        INSERT INTO operations (
            conversation_id
        )
        VALUES (%s)
        RETURNING id;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (conversation_id,)
            )

            resultado = cursor.fetchone()

    return resultado[0]


def vincular_cotacao_operacao(operation_id, quote_id):
    """
    Vincula uma cotação a uma operação.
    Impede duplicidade e verifica se ambos pertencem
    à mesma conversa.
    Retorna o ID do vínculo.
    """

    sql = """
        INSERT INTO operation_quotes (
            operation_id,
            quote_id
        )
        SELECT
            o.id,
            q.id
        FROM operations o
        INNER JOIN quotes q
            ON q.conversation_id = o.conversation_id
        WHERE
            o.id = %s
            AND q.id = %s

        ON CONFLICT (operation_id, quote_id)
        DO UPDATE SET
            operation_id = EXCLUDED.operation_id

        RETURNING id;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    operation_id,
                    quote_id
                )
            )

            resultado = cursor.fetchone()

    if not resultado:
        raise ValueError(
            "Operação ou cotação inexistente, "
            "ou pertencente a conversas diferentes."
        )

    return resultado[0]


def criar_operacao_com_cotacao(conversation_id, quote_id):
    """
    Cria uma operação e vincula a cotação.
    Se já existir uma operação criada para essa cotação,
    reutiliza a operação existente.
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            # Bloqueia a conversa durante a operação
            # para evitar criações simultâneas duplicadas.
            cursor.execute(
                """
                SELECT id
                FROM conversations
                WHERE id = %s
                FOR UPDATE;
                """,
                (conversation_id,)
            )

            conversa = cursor.fetchone()

            if not conversa:
                raise ValueError(
                    "Conversa não encontrada."
                )

            # Confirma que a cotação pertence à conversa.
            cursor.execute(
                """
                SELECT id
                FROM quotes
                WHERE
                    id = %s
                    AND conversation_id = %s;
                """,
                (
                    quote_id,
                    conversation_id
                )
            )

            cotacao = cursor.fetchone()

            if not cotacao:
                raise ValueError(
                    "Cotação inexistente ou pertencente "
                    "a outra conversa."
                )

            # Procura uma operação ainda criada
            # e já vinculada à mesma cotação.
            cursor.execute(
                """
                SELECT
                    o.id,
                    oq.id
                FROM operations o
                INNER JOIN operation_quotes oq
                    ON oq.operation_id = o.id
                WHERE
                    o.conversation_id = %s
                    AND oq.quote_id = %s
                    AND o.status = 'created'
                ORDER BY o.id DESC
                LIMIT 1;
                """,
                (
                    conversation_id,
                    quote_id
                )
            )

            existente = cursor.fetchone()

            if existente:
                return existente[0], existente[1]

            # Se não existir, cria uma nova operação.
            cursor.execute(
                """
                INSERT INTO operations (
                    conversation_id
                )
                VALUES (%s)
                RETURNING id;
                """,
                (conversation_id,)
            )

            operation_id = cursor.fetchone()[0]

            # Vincula a cotação à nova operação.
            cursor.execute(
                """
                INSERT INTO operation_quotes (
                    operation_id,
                    quote_id
                )
                VALUES (%s, %s)
                RETURNING id;
                """,
                (
                    operation_id,
                    quote_id
                )
            )

            vinculo_id = cursor.fetchone()[0]

    return operation_id, vinculo_id
    

##### CONSULTA DE COTAÇÕES #####

def obter_ultima_cotacao(conversation_id):
    """
    Busca a cotação mais recente de uma conversa.
    Retorna os dados da cotação ou None.
    """

    sql = """
        SELECT
            id,
            calculator_type,
            input_amount,
            result_data,
            rate_snapshot,
            status,
            created_at
        FROM quotes
        WHERE conversation_id = %s
        ORDER BY created_at DESC, id DESC
        LIMIT 1;
    """

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (conversation_id,)
            )

            resultado = cursor.fetchone()

    if not resultado:
        return None

    return {
        "id": resultado[0],
        "calculator_type": resultado[1],
        "input_amount": resultado[2],
        "result_data": resultado[3],
        "rate_snapshot": resultado[4],
        "status": resultado[5],
        "created_at": resultado[6]
    }
