from sheets import ler_taxas_remitflow


taxas = ler_taxas_remitflow()

print("Taxas lidas do Google Sheets:")
print()

print("G10 - BRL → VES:", taxas["taxa_brl_ves"])
print("F13 - VES → BRL:", taxas["taxa_ves_brl"])
print("F19 - BCV:", taxas["taxa_bcv"])
