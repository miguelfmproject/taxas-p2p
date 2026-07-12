from binance_ves import obter_taxas_ves
from bybit_brl import obter_taxas_brl


def main():

    print("===================================")
    print("      TAXAS P2P")
    print("===================================")

    ves = obter_taxas_ves()
    brl = obter_taxas_brl()

    print("\nResultado VES:")
    print(ves)

    print("\nResultado BRL:")
    print(brl)


if __name__ == "__main__":
    main()
