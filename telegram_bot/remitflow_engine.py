from decimal import Decimal, ROUND_DOWN, ROUND_UP


def arredondar_para_baixo(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


def arredondar_para_cima(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_UP)


def formatar_valor(valor):
    valor = Decimal(str(valor))
    valor = valor.quantize(Decimal("0.01"))

    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

#Calculadora 1
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

#Calculadora 2
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

#Calculadora 3
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

#Calculadora 4
def calcular_venezuela_brasil_dolar_bcv_a_reais(
    dolares_bcv,
    taxa_bcv,
    taxa_ves_brl
):
    dolares_bcv = Decimal(str(dolares_bcv))
    taxa_bcv = Decimal(str(taxa_bcv))
    taxa_ves_brl = Decimal(str(taxa_ves_brl))

    bolivares = arredondar_para_cima(dolares_bcv * taxa_bcv)
    reais = bolivares / taxa_ves_brl

    return {
        "dolares_bcv": dolares_bcv,
        "bolivares": bolivares,
        "reais": reais,
    }

#Calculadora 5
def calcular_venezuela_brasil_monto_en_bolivares(
    bolivares,
    taxa_bcv,
    taxa_ves_brl
):
    bolivares = Decimal(str(bolivares))
    taxa_bcv = Decimal(str(taxa_bcv))
    taxa_ves_brl = Decimal(str(taxa_ves_brl))

    dolar_bcv = bolivares / taxa_bcv
    reais = bolivares / taxa_ves_brl

    return {
        "bolivares": bolivares,
        "dolar_bcv": dolar_bcv,
        "reais": reais,
    }

#Calculadora 6
def calcular_venezuela_brasil_valor_a_receber_em_reais(
    reais,
    taxa_ves_brl,
    taxa_bcv
):
    reais = Decimal(str(reais))
    taxa_ves_brl = Decimal(str(taxa_ves_brl))
    taxa_bcv = Decimal(str(taxa_bcv))

    bolivares = arredondar_para_cima(reais * taxa_ves_brl)
    dolar_bcv = bolivares / taxa_bcv

    return {
        "reais": reais,
        "bolivares": bolivares,
        "dolar_bcv": dolar_bcv,
    }

#Mensagem Calculadora 1
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

#Mensagem Calculadora 2
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

#Mensagem Calculadora 3
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

#Mensagem Calculadora 4
def gerar_mensagem_venezuela_brasil_dolar_bcv_a_reais(resultado):
    dolares_bcv = formatar_valor(resultado["dolares_bcv"])
    bolivares = formatar_valor(resultado["bolivares"])
    reais = formatar_valor(resultado["reais"])

    return (
        "------- *Venezuela » Brasil Equiv Dólar BCV a Reais* -------\n\n"
        f"Si envían el equivalente a {dolares_bcv} Dólares BCV "
        f"({bolivares} Bolívares) desde Venezuela, "
        f"llega a Brasil {reais} Reais."
    )

#Mensagem Calculadora 5
def gerar_mensagem_venezuela_brasil_monto_en_bolivares(resultado):
    bolivares = formatar_valor(resultado["bolivares"])
    dolar_bcv = formatar_valor(resultado["dolar_bcv"])
    reais = formatar_valor(resultado["reais"])

    return (
        "------- *Venezuela » Brasil Monto en Bolívares* -------\n\n"
        f"Si envían {bolivares} Bolívares "
        f"(equivalente a {dolar_bcv} Dólares BCV) desde Venezuela, "
        f"llega a Brasil {reais} Reais."
    )

#Mensagem Calculadora 6



if __name__ == "__main__":
    taxa_brl_ves = "171.2"
    taxa_bcv = "814.6908"

    # Calculadora 1
    resultado1 = calcular_brasil_venezuela_dolar_final(
        reais="310",
        taxa_brl_ves=taxa_brl_ves,
        taxa_bcv=taxa_bcv
    )

    mensagem1 = gerar_mensagem_brasil_venezuela_dolar_final(resultado1)

    print(mensagem1)
    print()

    # Calculadora 2
    resultado2 = calcular_brasil_venezuela_dolar_a_receber(
        dolares_bcv="65.14",
        taxa_brl_ves=taxa_brl_ves,
        taxa_bcv=taxa_bcv
    )

    mensagem2 = gerar_mensagem_brasil_venezuela_dolar_a_receber(resultado2)

    print(mensagem2)
    print()

    # Calculadora 3
    resultado3 = calcular_brasil_venezuela_valor_bolivares_a_receber(
        bolivares="53072",
        taxa_brl_ves=taxa_brl_ves,
        taxa_bcv=taxa_bcv
    )

    mensagem3 = gerar_mensagem_brasil_venezuela_valor_bolivares_a_receber(resultado3)

    print(mensagem3)
