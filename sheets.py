import gspread

from google.oauth2.service_account import Credentials

from config import *


# =====================================================
# AUTENTICAÇÃO
# =====================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_file(
    "credentials/service_account.json",
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

planilha = gc.open_by_key(SPREADSHEET_ID)

aba = planilha.worksheet(SHEET_NAME)


# =====================================================
# ESCREVER VES
# =====================================================

def atualizar_ves(compra, venda, metodo_compra, metodo_venda):

    aba.update(CELL_VES_BUY, [[compra]])
    aba.update(CELL_VES_SELL, [[venda]])

    aba.update(CELL_VES_BUY_METHOD, [[metodo_compra]])
    aba.update(CELL_VES_SELL_METHOD, [[metodo_venda]])


# =====================================================
# ESCREVER BRL
# =====================================================

def atualizar_brl(compra, venda):

    aba.update(CELL_BRL_BUY, [[compra]])
    aba.update(CELL_BRL_SELL, [[venda]])
