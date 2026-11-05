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
    
