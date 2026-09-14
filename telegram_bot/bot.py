import requests
import json

from telegram_bot.remitflow_engine import (
    calcular_brasil_venezuela_dolar_final,
    calcular_brasil_venezuela_dolar_a_receber,
    calcular_brasil_venezuela_valor_bolivares_a_receber,
    calcular_venezuela_brasil_dolar_bcv_a_reais,
    calcular_venezuela_brasil_monto_en_bolivares,
    calcular_venezuela_brasil_valor_a_receber_em_reais,
    gerar_mensagem_brasil_venezuela_dolar_final,
    gerar_mensagem_brasil_venezuela_dolar_a_receber,
    gerar_mensagem_brasil_venezuela_valor_bolivares_a_receber,
    gerar_mensagem_venezuela_brasil_dolar_bcv_a_reais,
    gerar_mensagem_venezuela_brasil_monto_en_bolivares,
    gerar_mensagem_venezuela_brasil_valor_a_receber_em_reais,
)

from sheets import ler_taxas_remitflow


TOKEN = __import__("os").getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


# ============================================================
# ESTADO TEMPORÁRIO DOS CLIENTES
# ============================================================

clientes = {}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def enviar_mensagem(chat_id, texto, teclado=None):
    dados = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown"
    }

    if teclado:
        dados["reply_markup"] = json.dumps(teclado)

    requests.post(
        f"{BASE_URL}/sendMessage",
        data=dados,
        timeout=40
    )


def ler_taxas():
    taxas = ler_taxas_remitflow()

    return (
        taxas["taxa_brl_ves"],
        taxas["taxa_ves_brl"],
        taxas["taxa_bcv"]
    )


def converter_entrada_decimal(texto):
    """
    Aceita formatos como:
    310
    310,00
    310.00
    53.072,00
    50.000,00
    """

    texto = texto.strip().replace(" ", "")

    if "," in texto and "." in texto:
        # Exemplo: 53.072,00
        texto = texto.replace(".", "").replace(",", ".")

    elif "," in texto:
        # Exemplo: 310,00
        texto = texto.replace(",", ".")

    return texto


def teclado_inicio():
    return {
        "keyboard": [
            [{"text": "🇧🇷➡️🇻🇪 Cotización Brasil → Venezuela"}],
            [{"text": "🇻🇪➡️🇧🇷 Cotización Venezuela → Brasil"}],
            [{"text": "👤 Hablar directamente con Miguel"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


def teclado_brasil_venezuela():
    return {
        "keyboard": [
            [{"text": "💵 Reais a enviar para VZLA"}],
            [{"text": "💵 Dólar BCV a recibir en VZLA"}],
            [{"text": "🇻🇪 Bolívares a recibir en VZLA"}],
            [{"text": "🔙 Volver"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


def teclado_venezuela_brasil():
    return {
        "keyboard": [
            [{"text": "💵 Dólares BCV a Reais"}],
            [{"text": "🇻🇪 Bolívares a enviar"}],
            [{"text": "🇧🇷 Reais a recibir"}],
            [{"text": "🔙 Volver"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


# ============================================================
# MENSAGENS DE ORIENTAÇÃO
# ============================================================

def pedir_valor(chat_id, calculadora):
    clientes[chat_id] = {
        "etapa": "aguardando_valor",
        "calculadora": calculadora
    }

    if calculadora == 1:
        texto = (
            "💵 *Brasil » Venezuela Reais a enviar*\n\n"
            "Escribe el monto en *Reais* que deseas enviar para Venezuela."
        )

    elif calculadora == 2:
        texto = (
            "💵 *Brasil » Venezuela Equiv Dólar a recibir*\n\n"
            "Escribe el monto en *Dólares BCV* que deseas recibir en Venezuela."
        )

    else:
        texto = (
            "🇻🇪 *Brasil » Venezuela Bolívares a recibir*\n\n"
            "Escribe el monto en *Bolívares* que deseas que llegue a Venezuela."
        )

    enviar_mensagem(chat_id, texto)


# ============================================================
# PROCESSAMENTO DAS CALCULADORAS
# ============================================================

def processar_calculo(chat_id, texto):
    cliente = clientes.get(chat_id)

    if not cliente:
        return False

    calculadora = cliente["calculadora"]

    try:
        valor = converter_entrada_decimal(texto)

        # ----------------------------------------------------
        # LER AS TAXAS ATUAIS DO GOOGLE SHEETS
        # ----------------------------------------------------

        taxa_brl_ves, taxa_ves_brl, taxa_bcv = ler_taxas()

        # ----------------------------------------------------
        # CALCULADORA 1
        # ----------------------------------------------------

        if calculadora == 1:

            resultado = calcular_brasil_venezuela_dolar_final(
                reais=valor,
                taxa_brl_ves=taxa_brl_ves,
                taxa_bcv=taxa_bcv
            )

            mensagem = gerar_mensagem_brasil_venezuela_dolar_final(
                resultado
            )

        # ----------------------------------------------------
        # CALCULADORA 2
        # ----------------------------------------------------

        elif calculadora == 2:

            resultado = calcular_brasil_venezuela_dolar_a_receber(
                dolares_bcv=valor,
                taxa_brl_ves=taxa_brl_ves,
                taxa_bcv=taxa_bcv
            )

            mensagem = gerar_mensagem_brasil_venezuela_dolar_a_receber(
                resultado
            )

        # ----------------------------------------------------
        # CALCULADORA 3
        # ----------------------------------------------------

        elif calculadora == 3:

            resultado = calcular_brasil_venezuela_valor_bolivares_a_receber(
                bolivares=valor,
                taxa_brl_ves=taxa_brl_ves,
                taxa_bcv=taxa_bcv
            )

            mensagem = (
                gerar_mensagem_brasil_venezuela_valor_bolivares_a_receber(
                    resultado
                )
            )

        else:
            return False

        # ----------------------------------------------------
        # ENVIAR RESULTADO
        # ----------------------------------------------------

        enviar_mensagem(
            chat_id,
            mensagem,
            teclado_brasil_venezuela()
        )

        clientes.pop(chat_id, None)

        return True

    except Exception as erro:

        print("\nERRO AO CALCULAR:")
        print(erro)

        enviar_mensagem(
            chat_id,
            "❌ No pude realizar el cálculo.\n\n"
            "Por favor, verifica el valor informado e inténtalo nuevamente."
        )

        return True


# ============================================================
# PROCESSAMENTO DAS MENSAGENS
# ============================================================

def processar_mensagem(chat_id, texto):

    # --------------------------------------------------------
    # SE ESTÁ AGUARDANDO UM VALOR
    # --------------------------------------------------------

    if chat_id in clientes:
        if clientes[chat_id]["etapa"] == "aguardando_valor":
            return processar_calculo(chat_id, texto)

    # --------------------------------------------------------
    # /start
    # --------------------------------------------------------

    if texto == "/start":

        clientes.pop(chat_id, None)

        enviar_mensagem(
            chat_id,
            "¡Hola! 👋 Bienvenido a MiguelFM.\n\n"
            "¿Qué deseas hacer?",
            teclado_inicio()
        )

        return True

    # --------------------------------------------------------
    # BRASIL → VENEZUELA
    # --------------------------------------------------------

    if texto == "🇧🇷➡️🇻🇪 Cotización Brasil → Venezuela":

        enviar_mensagem(
            chat_id,
            "🇧🇷➡️🇻🇪 *Brasil → Venezuela*\n\n"
            "Selecciona el tipo de cotización:",
            teclado_brasil_venezuela()
        )

        return True

    # --------------------------------------------------------
    # CALCULADORA 1
    # --------------------------------------------------------

    if texto == "💵 Equiv. Dólar Final":

        pedir_valor(chat_id, 1)
        return True

    # --------------------------------------------------------
    # CALCULADORA 2
    # --------------------------------------------------------

    if texto == "💵 Dólar a recibir":

        pedir_valor(chat_id, 2)
        return True

    # --------------------------------------------------------
    # CALCULADORA 3
    # --------------------------------------------------------

    if texto == "🇻🇪 Bolívares a recibir":

        pedir_valor(chat_id, 3)
        return True

    # --------------------------------------------------------
    # VENEZUELA → BRASIL
    # --------------------------------------------------------

    if texto == "🇻🇪➡️🇧🇷 Cotización Venezuela → Brasil":

        enviar_mensagem(
            chat_id,
            "🇻🇪➡️🇧🇷 Esta opción estará disponible próximamente."
        )

        return True

    # --------------------------------------------------------
    # FALAR COM MIGUEL
    # --------------------------------------------------------

    if texto == "👤 Hablar directamente con Miguel":

        enviar_mensagem(
            chat_id,
            "👤 Para hablar directamente con Miguel, "
            "por favor espera las instrucciones de contacto."
        )

        return True

    # --------------------------------------------------------
    # VOLTAR
    # --------------------------------------------------------

    if texto == "🔙 Volver":

        clientes.pop(chat_id, None)

        enviar_mensagem(
            chat_id,
            "Volviendo al menú principal...",
            teclado_inicio()
        )

        return True

    return False


# ============================================================
# LOOP PRINCIPAL DO BOT
# ============================================================

def main():

    offset = None

    print("MiguelFM iniciado. Aguardando mensajes...")

    while True:

        try:

            resposta = requests.get(
                f"{BASE_URL}/getUpdates",
                params={
                    "offset": offset,
                    "timeout": 30
                },
                timeout=40
            )

            dados = resposta.json()

            for atualizacao in dados.get("result", []):

                offset = atualizacao["update_id"] + 1

                mensagem = atualizacao.get("message")

                if not mensagem:
                    continue

                chat_id = mensagem["chat"]["id"]
                texto = mensagem.get("text", "")

                if not texto:
                    continue

                print(
                    f"Mensagem recebida de {chat_id}: {texto}"
                )

                processar_mensagem(chat_id, texto)

        except Exception as erro:

            print("\nERRO NO BOT:")
            print(erro)

            # Evita que um erro isolado encerre o bot.
            import time
            time.sleep(3)


if __name__ == "__main__":
    main()
