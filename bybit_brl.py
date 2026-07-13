import requests
from statistics import mean
from collections import Counter
import math

URL = "https://www.bybit.com/x-api/fiat/otc/item/online"


def calcular_taxa(side):

    # Configuração
    if side == 1:          # Compra
        TOTAL_ANUNCIOS = 100
    else:                  # Venda
        TOTAL_ANUNCIOS = 15

    ANUNCIOS_MEDIA = 5

    payload = {
        "userId": "",
        "tokenId": "USDT",
        "currencyId": "BRL",
        "payment": [],
        "side": str(side),
        "size": str(TOTAL_ANUNCIOS),
        "page": "1",
        "amount": "",
        "sortType": "OVERALL_RANKING",
        "itemRegion": 1,
        "authMaker": False,
        "bulkMaker": False,
        "canTrade": False,
        "countryCode": "",
        "paymentPeriod": [],
        "tradeWith": False,
        "vaMaker": False,
        "verificationFilter": 0
    }

    resposta = requests.post(URL, json=payload)
    dados = resposta.json()

    anuncios = dados["result"]["items"]

    print("=" * 60)
    print("SIDE =", side)
    print("Total anúncios:", len(anuncios))

    # Descobrir predominância
    inteiros = [int(float(x["price"])) for x in anuncios]

    predominancia = Counter(inteiros).most_common(1)[0][0]

    filtro = (predominancia + 1) * 100

    print("Predominância:", predominancia)
    print("Filtro automático:", filtro)

    # Filtrar anúncios
    validos = []

    for anuncio in anuncios:

        minimo = float(anuncio["minAmount"])
        maximo = float(anuncio["maxAmount"])

        if minimo <= filtro <= maximo:
            validos.append(anuncio)

    print("Anúncios válidos:", len(validos))

    # Ordenação
    if side == 1:
        # Compra → menor preço primeiro
        validos = sorted(
            validos,
            key=lambda x: float(x["price"])
        )
    else:
        # Venda → maior preço primeiro
        validos = sorted(
            validos,
            key=lambda x: float(x["price"]),
            reverse=True
        )

    top = validos[:ANUNCIOS_MEDIA]

    print(f"\n{ANUNCIOS_MEDIA} anúncios utilizados:\n")

    for i, anuncio in enumerate(top, start=1):

        print(
            f"{i:02d}",
            anuncio["nickName"],
            "|",
            anuncio["price"],
            "|",
            anuncio["minAmount"],
            "-",
            anuncio["maxAmount"]
        )

    precos = [float(x["price"]) for x in top]

    media = mean(precos)

    compra = math.ceil(media * 100) / 100
    venda = math.floor(media * 100) / 100

    print("\nMédia:", media)

    if side == 1:
        print("Compra:", compra)
        taxa = compra
    else:
        print("Venda:", venda)
        taxa = venda

    return {
        "media": media,
        "taxa": taxa,
        "filtro": filtro
    }


# ==========================
# TESTE COMPRA
# ==========================

resultado_compra = calcular_taxa(1)

print("\nResultado final (Compra):")
print(f"Taxa de compra: {resultado_compra['taxa']}")
print(f"Filtro: {resultado_compra['filtro']}")

# ==========================
# TESTE VENDA
# ==========================

resultado_venda = calcular_taxa(0)

print("\nResultado final (Venda):")
print(f"Taxa de venda: {resultado_venda['taxa']}")
print(f"Filtro: {resultado_venda['filtro']}")
