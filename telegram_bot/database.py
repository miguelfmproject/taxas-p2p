import os

import psycopg


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
    
