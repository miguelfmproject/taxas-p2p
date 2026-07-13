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

        print(
            f"Página {pagina} - Status:",
            resposta.status_code
        )

        dados = resposta.json()

        if dados.get("data"):

            anuncios.extend(
                dados["data"]
            )

    print()

    print(
        "Total de anúncios:",
        len(anuncios)
    )

    return anuncios

# =====================================================
# MÉTODOS DE PAGAMENTO
# =====================================================

def tem_metodo_valido(
        anuncio,
        metodos_validos
):

    for metodo in anuncio["adv"]["tradeMethods"]:

        if metodo["tradeMethodName"] in metodos_validos:

            return True

    return False

# =====================================================
# FILTRO APENAS POR MÉTODOS
# =====================================================

def filtrar_metodos(
        anuncios,
        metodos_validos
):

    retorno = []

    for anuncio in anuncios:

        if tem_metodo_valido(
            anuncio,
            metodos_validos
        ):

            retorno.append(
                anuncio
            )

    return retorno

# =====================================================
# MEDIANA DO MERCADO
# =====================================================

def estimativa_inicial(validos):

    precos = []

    for anuncio in validos:

        precos.append(

            float(
                anuncio["adv"]["price"]
            )

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
# FILTRA PELO VALOR DE BUSCA
# =====================================================

def filtrar_por_valor(
        anuncios,
        valor_buscado
):

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


# =====================================================
# PROCURA PREDOMINÂNCIA
# =====================================================

def procurar_predominancia(validos):

    if len(validos) < 4:

        return None


    for i in range(len(validos) - 3):

        g1 = inteiro_taxa(
            float(validos[i]["adv"]["price"])
        )

        g2 = inteiro_taxa(
            float(validos[i + 1]["adv"]["price"])
        )

        g3 = inteiro_taxa(
            float(validos[i + 2]["adv"]["price"])
        )


        if g1 == g2 == g3:

            return {

                "grupo": g1,

                "anuncio": validos[i + 3]

            }

    return None


# =====================================================
# BUSCA INTELIGENTE
# =====================================================

def busca_convergente(anuncios_filtrados):

    historico = []

    estimativa = estimativa_inicial(
        anuncios_filtrados
    )

    grupo = inteiro_taxa(
        estimativa
    )


    for tentativa in range(TENTATIVAS_MAXIMAS):

        valor = valor_busca(
            grupo
        )

        candidatos = filtrar_por_valor(
            anuncios_filtrados,
            valor
        )

        predominancia = procurar_predominancia(
            candidatos
        )

        historico.append({

            "tentativa": tentativa + 1,

            "grupo_pesquisado": grupo,

            "valor": valor,

            "quantidade": len(candidatos),

            "predominancia":
                None
                if predominancia is None
                else predominancia["grupo"]

        })

        if predominancia is None:

            break

        novo_grupo = predominancia["grupo"]

        if novo_grupo == grupo:

            anuncio = predominancia["anuncio"]

            return {

                "taxa": float(
                    anuncio["adv"]["price"]
                ),

                "grupo": grupo,

                "metodo": "CONVERGÊNCIA",

                "anuncio": anuncio,

                "historico": historico

            }

        grupo = novo_grupo


    return {

        "taxa": estimativa,

        "grupo": inteiro_taxa(
            estimativa
        ),

        "metodo": "MEDIANA",

        "anuncio": None,

        "historico": historico

    }
# =====================================================
# COMPRA USDT (BUY)
# =====================================================

def comprar_usdt_ves():

    anuncios = buscar_anuncios(
        "VES",
        "BUY"
    )

    metodos = [
        "Pago Movil"
    ]

    anuncios = filtrar_metodos(
        anuncios,
        metodos
    )

    print()

    print(
        "Compra - anúncios após filtro:",
        len(anuncios)
    )

    resultado = busca_convergente(
        anuncios
    )

    return resultado


# =====================================================
# VENDA USDT (SELL)
# =====================================================

def vender_usdt_ves():

    anuncios = buscar_anuncios(
        "VES",
        "SELL"
    )

    metodos = [

        "Banco de Venezuela",

        "Pago Movil",

        "Bank Transfer"

    ]

    anuncios = filtrar_metodos(
        anuncios,
        metodos
    )

    print()

    print(
        "Venda - anúncios após filtro:",
        len(anuncios)
    )

    resultado = busca_convergente(
        anuncios
    )

    return resultado
# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================

def obter_taxas_ves():

    compra = comprar_usdt_ves()

    venda = vender_usdt_ves()

    return {

        "buy": compra["taxa"],

        "sell": venda["taxa"],

        "buy_method": compra["metodo"],

        "sell_method": venda["metodo"]

    }
