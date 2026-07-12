import requests
import json
from statistics import median

# =====================================================
# CONFIGURAÇÕES
# =====================================================

PAGINAS = 5
ROWS = 20

TENTATIVAS_MAXIMAS = 8

URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

HEADERS = {
    "Content-Type": "application/json"
}

# =====================================================
# BUSCA BINANCE
# =====================================================

def buscar_anuncios(fiat, trade_type):

    anuncios = []

    for pagina in range(1, PAGINAS + 1):

        payload = {

            "asset": "USDT",

            "fiat": fiat,

            "tradeType": trade_type,

            "page": pagina,

            "rows": ROWS,

            "payTypes": [],

            "publisherType": None,

            "transAmount": ""

        }

        resposta = requests.post(

            URL,

            headers=HEADERS,

            data=json.dumps(payload)

        )

        dados = resposta.json()

        if dados.get("data"):

            anuncios.extend(
                dados["data"]
            )

    return anuncios
