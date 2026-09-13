from sheets import ler_taxas_remitflow

from telegram_bot.remitflow_engine import (
    calcular_brasil_venezuela_dolar_final,
    calcular_brasil_venezuela_dolar_a_receber,
    calcular_brasil_venezuela_valor_bolivares_a_receber,
    calcular_venezuela_brasil_dolar_bcv_a_reais,
    calcular_venezuela_brasil_monto_en_bolivares,
    calcular_venezuela_brasil_valor_a_receber_em_reais,
)


# ============================================================
# LER TAXAS DIRETAMENTE DO GOOGLE SHEETS
# ============================================================

taxas = ler_taxas_remitflow()

taxa_brl_ves = taxas["taxa_brl_ves"]
taxa_ves_brl = taxas["taxa_ves_brl"]
taxa_bcv = taxas["taxa_bcv"]


print()
print("========================================")
print("TAXAS LIDAS DO GOOGLE SHEETS")
print("========================================")

print("G10 - BRL → VES:", taxa_brl_ves)
print("F13 - VES → BRL:", taxa_ves_brl)
print("F19 - BCV:", taxa_bcv)


# ============================================================
# TESTE 1
# ============================================================

resultado1 = calcular_brasil_venezuela_dolar_final(
    reais="310",
    taxa_brl_ves=taxa_brl_ves,
    taxa_bcv=taxa_bcv
)

print()
print("========================================")
print("CALCULADORA 1")
print("========================================")
print("Entrada: R$ 310,00")
print("Resultado:", resultado1)


# ============================================================
# TESTE 2
# ============================================================

resultado2 = calcular_brasil_venezuela_dolar_a_receber(
    dolares_bcv="65.14",
    taxa_brl_ves=taxa_brl_ves,
    taxa_bcv=taxa_bcv
)

print()
print("========================================")
print("CALCULADORA 2")
print("========================================")
print("Entrada: US$ 65,14")
print("Resultado:", resultado2)


# ============================================================
# TESTE 3
# ============================================================

resultado3 = calcular_brasil_venezuela_valor_bolivares_a_receber(
    bolivares="53072",
    taxa_brl_ves=taxa_brl_ves,
    taxa_bcv=taxa_bcv
)

print()
print("========================================")
print("CALCULADORA 3")
print("========================================")
print("Entrada: Bs 53.072,00")
print("Resultado:", resultado3)


# ============================================================
# TESTE 4
# ============================================================

resultado4 = calcular_venezuela_brasil_dolar_bcv_a_reais(
    dolares_bcv="61.37",
    taxa_bcv=taxa_bcv,
    taxa_ves_brl=taxa_ves_brl
)

print()
print("========================================")
print("CALCULADORA 4")
print("========================================")
print("Entrada: US$ 61,37")
print("Resultado:", resultado4)


# ============================================================
# TESTE 5
# ============================================================

resultado5 = calcular_venezuela_brasil_monto_en_bolivares(
    bolivares="50000",
    taxa_bcv=taxa_bcv,
    taxa_ves_brl=taxa_ves_brl
)

print()
print("========================================")
print("CALCULADORA 5")
print("========================================")
print("Entrada: Bs 50.000,00")
print("Resultado:", resultado5)


# ============================================================
# TESTE 6
# ============================================================

resultado6 = calcular_venezuela_brasil_valor_a_receber_em_reais(
    reais="245.82",
    taxa_ves_brl=taxa_ves_brl,
    taxa_bcv=taxa_bcv
)

print()
print("========================================")
print("CALCULADORA 6")
print("========================================")
print("Entrada: R$ 245,82")
print("Resultado:", resultado6)


print()
print("========================================")
print("TESTE CONCLUÍDO")
print("========================================")
