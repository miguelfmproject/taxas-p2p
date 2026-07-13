import gspread

from google.oauth2.service_account import Credentials

from config import SHEET_ID


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


credenciais = Credentials.from_service_account_file(
    "credentials/service_account.json",
    scopes=SCOPES
)

cliente = gspread.authorize(credenciais)

planilha = cliente.open_by_key(SHEET_ID)

aba = planilha.sheet1


def atualizar_ves(compra, venda, metodo_compra, metodo_venda):

    aba.update("I8", compra)

    aba.update("J8", venda)

    aba.update("I10", metodo_compra)

    aba.update("J10", metodo_venda)


def atualizar_brl(compra, venda):

    aba.update("K8", compra)

    aba.update("L8", venda)
