from binance_ves import obter_taxas_ves
from bybit_brl import obter_taxas_brl
from sheets import atualizar_ves
from sheets import atualizar_brl
from sheets import atualizar_status

import traceback


def main():

    print("=" * 60)
    print("ATUALIZANDO TAXAS P2P")
    print("=" * 60)

    print("\nBuscando Binance (VES)...")
    ves = obter_taxas_ves()

    print("\nBuscando Bybit (BRL)...")
    brl = obter_taxas_brl()

    print("\nAtualizando Google Sheets...")

    try:

        atualizar_ves(
            ves["buy"],
            ves["sell"],
            ves["buy_method"],
            ves["sell_method"]
        )

        atualizar_brl(
            brl["buy"],
            brl["sell"]
        )
        
        atualizar_status("OK")

        print("\nGoogle Sheets atualizado com sucesso!")

    except Exception:

        print("\n==============================")
        print("ERRO AO ATUALIZAR GOOGLE SHEETS")
        print("==============================\n")

        traceback.print_exc()
        
        atualizar_status("ERRO")

        raise

    print()
    print("=" * 60)
    print("ATUALIZAÇÃO CONCLUÍDA")
    print("=" * 60)

    print()
    print("VES BUY :", ves["buy"])
    print("VES SELL:", ves["sell"])
    print("BRL BUY :", brl["buy"])
    print("BRL SELL:", brl["sell"])


if __name__ == "__main__":
    main()
