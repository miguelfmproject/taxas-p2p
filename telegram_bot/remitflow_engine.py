from decimal import Decimal, ROUND_DOWN, ROUND_UP


def arredondar_para_baixo(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


def arredondar_para_cima(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_UP)


def formatar_valor(valor):
    valor = Decimal(str(valor))
    valor = valor.quantize(Decimal("0.01"))

    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_brasil_venezuela_dolar_final(reais, taxa_brl_ves, taxa_bcv):
    reais = Decimal(str(reais))
    taxa_brl_ves = Decimal(str(taxa_brl_ves))
    taxa_bcv = Decimal(str(taxa_bcv))

    bolivares = reais * taxa_brl_ves
    dolar_bcv = arredondar_para_baixo(bolivares / taxa_bcv)

    return {
        "reais": reais,
        "bolivares": bolivares,
        "dolar_bcv": dolar_bcv,
    }


if __name__ == "__main__":
    resultado = calcular_brasil_venezuela_dolar_final(
        reais="310",
        taxa_brl_ves="170.4",
        taxa_bcv="596.7824"
    )

    print(formatar_valor("310"))
print(formatar_valor("52824"))
print(formatar_valor("88.51"))
