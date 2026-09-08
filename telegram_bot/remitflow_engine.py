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


def calcular_brasil_venezuela_dolar_a_receber(
    dolares_bcv,
    taxa_brl_ves,
    taxa_bcv
):
    dolares_bcv = Decimal(str(dolares_bcv))
    taxa_brl_ves = Decimal(str(taxa_brl_ves))
    taxa_bcv = Decimal(str(taxa_bcv))

    bolivares = dolares_bcv * taxa_bcv
    reais = arredondar_para_cima(bolivares / taxa_brl_ves)

    return {
        "dolares_bcv": dolares_bcv,
        "bolivares": bolivares,
        "reais": reais,
    }


def calcular_brasil_venezuela_valor_bolivares_a_receber(
    bolivares,
    taxa_brl_ves,
    taxa_bcv
):
    bolivares = Decimal(str(bolivares))
    taxa_brl_ves = Decimal(str(taxa_brl_ves))
    taxa_bcv = Decimal(str(taxa_bcv))

    dolar_bcv = bolivares / taxa_bcv
    reais = arredondar_para_cima(bolivares / taxa_brl_ves)

    return {
        "bolivares": bolivares,
        "dolar_bcv": dolar_bcv,
        "reais": reais,
    }


def gerar_mensagem_brasil_venezuela_dolar_final(resultado):
    reais = formatar_valor(resultado["reais"])
    bolivares = formatar_valor(resultado["bolivares"])
    dolar_bcv = formatar_valor(resultado["dolar_bcv"])

    return (
        "------- *Brasil » Venezuela Equiv Dólar Final* -------\n\n"
        f"Si envían {reais} Reais hacia Venezuela, "
        f"llega {bolivares} Bolívares "
        f"(equivalente a {dolar_bcv} Dólares BCV)."
    )


def gerar_mensagem_brasil_venezuela_dolar_a_receber(resultado):
    dolares_bcv = formatar_valor(resultado["dolares_bcv"])
    bolivares = formatar_valor(resultado["bolivares"])
    reais = formatar_valor(resultado["reais"])

    return (
        "------- *Brasil » Venezuela Equiv Dólar a recibir* -------\n\n"
        f"Para que llegue el equivalente a {dolares_bcv} Dólares BCV "
        f"({bolivares} Bolívares) a Venezuela, "
        f"tienen que enviar {reais} Reais."
    )


def gerar_mensagem_brasil_venezuela_valor_bolivares_a_receber(resultado):
    bolivares = formatar_valor(resultado["bolivares"])
    dolar_bcv = formatar_valor(resultado["dolar_bcv"])
    reais = formatar_valor(resultado["reais"])

    return (
        "------- *Brasil » Venezuela Valor Bolívares a Recibir* -------\n\n"
        f"Para que llegue {bolivares} Bolívares a Venezuela "
        f"(equivalente a {dolar_bcv} Dólares BCV), "
        f"tienen que enviar {reais} Reais."
    )


if __name__ == "__main__":
    resultado = calcular_brasil_venezuela_dolar_final(
        reais="310",
        taxa_brl_ves="170.4",
        taxa_bcv="596.7824"
    )

    mensagem = gerar_mensagem_brasil_venezuela_dolar_final(resultado)

    print(mensagem)
