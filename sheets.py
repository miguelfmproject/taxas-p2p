import gspread
from google.oauth2.service_account import Credentials
import traceback

from config import SPREADSHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def conectar():

    try:

        credenciais = Credentials.from_service_account_file(
            "credentials/service_account.json",
            scopes=SCOPES
        )

        cliente = gspread.authorize(credenciais)

        planilha = cliente.open_by_key(SPREADSHEET_ID)

        return planilha.sheet1

    except Exception:

        print("\nERRO AO CONECTAR COM GOOGLE SHEETS\n")

        traceback.print_exc()

        raise


def atualizar_ves(compra, venda, metodo_compra, metodo_venda):

    aba = conectar()

    aba.update("I8", [[compra]])
    aba.update("J8", [[venda]])
    aba.update("I10", [[metodo_compra]])
    aba.update("J10", [[metodo_venda]])


def atualizar_brl(compra, venda):

    aba = conectar()

    aba.update("K8", [[compra]])
    aba.update("L8", [[venda]])
