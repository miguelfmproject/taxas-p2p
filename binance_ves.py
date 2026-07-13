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
# =====================================================
# MÉTODOS DE PAGAMENTO
# =====================================================

def tem_metodo_valido(anuncio, metodos_validos):

    for metodo in anuncio["adv"]["tradeMethods"]:

        if metodo["tradeMethodName"] in metodos_validos:
            return True

    return False


# =====================================================
# FILTRO POR MÉTODOS
# =====================================================

def filtrar_metodos(anuncios, metodos_validos):

    retorno = []

    for anuncio in anuncios:

        if tem_metodo_valido(anuncio, metodos_validos):
            retorno.append(anuncio)

    return retorno


# =====================================================
# MEDIANA DO MERCADO
# =====================================================

def estimativa_inicial(validos):

    precos = []

    for anuncio in validos:

        precos.append(
            float(anuncio["adv"]["price"])
        )

    return median(precos)


# =====================================================
# REMOVE DECIMAIS
# =====================================================

def inteiro_taxa(valor):

    return int(valor)


# =====================================================
# VALOR DE BUSCA
# =====================================================

def valor_busca(grupo):

    return grupo * 100


# =====================================================
# FILTRO PELO VALOR
# =====================================================

def filtrar_por_valor(anuncios, valor_buscado):

    validos = []

    for anuncio in anuncios:

        minimo = float(
            anuncio["adv"]["minSingleTransAmount"]
        )

        maximo = float(
            anuncio["adv"]["dynamicMaxSingleTransAmount"]
        )

        if minimo <= valor_buscado <= maximo:
            validos.append(anuncio)

    return validos
