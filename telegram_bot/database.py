
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
  
