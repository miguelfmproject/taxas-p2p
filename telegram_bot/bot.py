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


def teclado_cotizacion():
    return {
        "keyboard": [
            [{"text": "🇧🇷➡️🇻🇪 Cotización Brasil → Venezuela"}],
            [{"text": "🇻🇪➡️🇧🇷 Cotización Venezuela → Brasil"}],
            [{"text": "🔙 Volver"}]
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
            [{"text": "💵 Equivalente en Dólares BCV a convertir en Reais"}],
            [{"text": "🇻🇪 Bolívares a enviar desde Vzla"}],
            [{"text": "🇧🇷 Reais a recibir en Brasil"}],
            [{"text": "🔙 Volver"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


# ============================================================
# MENSAGENS DE ORIENTAÇÃO
# ============================================================

def pedir_valor(chat_id, calculadora):

    if calculadora <= 3:
        direcao = "brasil_venezuela"
    else:
        direcao = "venezuela_brasil"

    clientes[chat_id] = {
        "etapa": "aguardando_valor",
        "calculadora": calculadora,
        "direcao": direcao
    }

    if calculadora == 1:
        texto = (
            "💵 *Brasil » Venezuela Reais a enviar*\n\n"
            "Escribe ÚNICAMENTE el monto en *Reais* que deseas enviar para Venezuela."
        )

    elif calculadora == 2:
        texto = (
            "💵 *Brasil » Venezuela Dólares BCV a recibir*\n\n"
            "Escribe ÚNICAMENTE el monto en *Dólares BCV* que deseas recibir en Venezuela."
        )

    elif calculadora == 3:
        texto = (
            "🇻🇪 *Brasil » Venezuela Bolívares a recibir*\n\n"
            "Escribe ÚNICAMENTE el monto en *Bolívares* que deseas que llegue a Venezuela."
        )

    elif calculadora == 4:
        texto = (
            "💵 *Venezuela » Brasil Dólares BCV a Reais*\n\n"
            "Escribe ÚNICAMENTE el monto en *Dólares BCV* que deseas convertir a Reais."
        )

    elif calculadora == 5:
        texto = (
            "🇻🇪 *Venezuela » Brasil Bolívares a enviar*\n\n"
            "Escribe ÚNICAMENTE el monto en *Bolívares* que deseas enviar desde Venezuela."
        )

    elif calculadora == 6:
        texto = (
            "🇧🇷 *Venezuela » Brasil Reais a recibir*\n\n"
            "Escribe ÚNICAMENTE el monto en *Reais* que deseas recibir en Brasil."
        )

    else:
        clientes.pop(chat_id, None)
        return

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
        # BRASIL → VENEZUELA
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

        elif calculadora == 2:

            resultado = calcular_brasil_venezuela_dolar_a_receber(
                dolares_bcv=valor,
                taxa_brl_ves=taxa_brl_ves,
                taxa_bcv=taxa_bcv
            )

            mensagem = gerar_mensagem_brasil_venezuela_dolar_a_receber(
                resultado
            )

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

        # ----------------------------------------------------
        # VENEZUELA → BRASIL
        # ----------------------------------------------------

        elif calculadora == 4:

            resultado = calcular_venezuela_brasil_dolar_bcv_a_reais(
                dolares_bcv=valor,
                taxa_bcv=taxa_bcv,
                taxa_ves_brl=taxa_ves_brl
            )

            mensagem = gerar_mensagem_venezuela_brasil_dolar_bcv_a_reais(
                resultado
            )

        elif calculadora == 5:

            resultado = calcular_venezuela_brasil_monto_en_bolivares(
                bolivares=valor,
                taxa_bcv=taxa_bcv,
                taxa_ves_brl=taxa_ves_brl
            )

            mensagem = gerar_mensagem_venezuela_brasil_monto_en_bolivares(
                resultado
            )

        elif calculadora == 6:

            resultado = calcular_venezuela_brasil_valor_a_receber_em_reais(
                reais=valor,
                taxa_ves_brl=taxa_ves_brl,
                taxa_bcv=taxa_bcv
            )

            mensagem = gerar_mensagem_venezuela_brasil_valor_a_receber_em_reais(
                resultado
            )

        else:
            return False

        # ----------------------------------------------------
        # ENVIAR RESULTADO
        # ----------------------------------------------------

        if calculadora <= 3:
            teclado = teclado_brasil_venezuela()
        else:
            teclado = teclado_venezuela_brasil()

        enviar_mensagem(
            chat_id,
            mensagem,
            teclado
        )

        clientes.pop(chat_id, None)

        return True

    except Exception as erro:

        print("\nERRO AO CALCULAR:")
        print(erro)

        enviar_mensagem(
            chat_id,
            "❌ No conseguí realizar el cálculo.\n\n"
            "Por favor escribe únicamente en números el valor solicitado; o selecciona en las opciones de abajo ⬇️⬇️ o en el menú lateral ↖️↖️ alguna otra opción."
        )

        return True


# ============================================================
# PROCESSAMENTO DAS MENSAGENS
# ============================================================

def processar_mensagem(chat_id, texto):

    # Normaliza espaços acidentais enviados pelo Telegram.
    texto = texto.strip()

    # ========================================================
    # PRIORIDADE ABSOLUTA — FALAR COM MIGUEL
    #
    # Deve funcionar independentemente do estado atual:
    # menu principal, menu de cotização ou aguardando valor.
    #
    # O startswith() evita que pequenas diferenças posteriores
    # no texto do botão façam a mensagem cair no calculador.
    # ========================================================

    if texto.startswith("👤 Hablar directamente con Miguel"):

        clientes.pop(chat_id, None)

        enviar_mensagem(
            chat_id,
            "👤 Para hablar directamente con Miguel, "
            "toca en el siguiente enlace: https://wa.me/qr/BYH3M7JCHI7DA1"
        )

        return True

    # --------------------------------------------------------
    # START — PRIORIDADE MÁXIMA
    # Cancela qualquer operação em andamento.
    # --------------------------------------------------------

    if texto == "/start":

        clientes.pop(chat_id, None)

        enviar_mensagem(
            chat_id,
            "¡Hola! 👋 Bienvenido al bot secuencial automatizado de 🔰MiguelFM Remesas.\n\n"
            "Por favor selecciona en las opciones abajo ⬇️⬇️⬇️ lo que deseas hacer.",
            teclado_inicio()
        )

        return True

    # --------------------------------------------------------
    # COTIZACIÓN — PRIORIDADE MÁXIMA
    # Cancela qualquer operação em andamento.
    # Vai diretamente para escolha da direção.
    # --------------------------------------------------------

    if texto == "/cotizacion":

        clientes.pop(chat_id, None)

        enviar_mensagem(
            chat_id,
            "Selecciona el tipo de cotización:",
            teclado_cotizacion()
        )

        return True

    # --------------------------------------------------------
    # ATENDENTE — PRIORIDADE MÁXIMA
    # Cancela qualquer operação em andamento.
    # --------------------------------------------------------

    if texto == "/atendiente":

        clientes.pop(chat_id, None)

        enviar_mensagem(
            chat_id,
            "👤 Para hablar directamente con Miguel, "
            "toca en el siguiente enlace: https://wa.me/qr/BYH3M7JCHI7DA1"
        )

        return True

    # --------------------------------------------------------
    # AYUDA — PRIORIDADE MÁXIMA
    # Cancela qualquer operação em andamento.
    # --------------------------------------------------------

    if texto == "/ayuda":

        clientes.pop(chat_id, None)

        enviar_mensagem(
            chat_id,
            "ℹ️ *Ayuda e información*\n\n"
            "Selecciona una opción del menú para solicitar una cotización "
            "o hablar directamente con Miguel."
        )

        return True

    # --------------------------------------------------------
    # VOLVER
    # Se estiver dentro de uma direção, retorna ao menu
    # daquela direção.
    # Caso contrário, retorna ao menu principal.
    # --------------------------------------------------------

    if texto == "🔙 Volver":

        cliente = clientes.get(chat_id)

        if cliente and cliente.get("direcao") == "brasil_venezuela":

            enviar_mensagem(
                chat_id,
                "🇧🇷➡️🇻🇪 *Brasil → Venezuela*\n\n"
                "Selecciona el tipo de cotización:",
                teclado_brasil_venezuela()
            )

        elif cliente and cliente.get("direcao") == "venezuela_brasil":

            enviar_mensagem(
                chat_id,
                "🇻🇪➡️🇧🇷 *Venezuela → Brasil*\n\n"
                "Selecciona el tipo de cotización:",
                teclado_venezuela_brasil()
            )

        else:

            enviar_mensagem(
                chat_id,
                "Volviendo al menú principal...",
                teclado_inicio()
            )

        clientes.pop(chat_id, None)

        return True

    # --------------------------------------------------------
    # CLIENTE JÁ ESTÁ EM UMA CALCULADORA
    # --------------------------------------------------------

    if chat_id in clientes:

        if clientes[chat_id]["etapa"] == "aguardando_valor":
            return processar_calculo(chat_id, texto)

    # --------------------------------------------------------
    # BRASIL → VENEZUELA
    # --------------------------------------------------------

    if texto == "🇧🇷➡️🇻🇪 Cotización Brasil → Venezuela":

        clientes[chat_id] = {
            "etapa": "menu",
            "direcao": "brasil_venezuela"
        }

        enviar_mensagem(
            chat_id,
            "🇧🇷➡️🇻🇪 *Brasil → Venezuela*\n\n"
            "Selecciona el tipo de cotización:",
            teclado_brasil_venezuela()
        )

        return True

    if texto == "💵 Reais a enviar para VZLA":

        pedir_valor(chat_id, 1)

        return True

    if texto == "💵 Dólar BCV a recibir en VZLA":

        pedir_valor(chat_id, 2)

        return True

    if texto == "🇻🇪 Bolívares a recibir en VZLA":

        pedir_valor(chat_id, 3)

        return True

    # --------------------------------------------------------
    # VENEZUELA → BRASIL
    # --------------------------------------------------------

    if texto == "🇻🇪➡️🇧🇷 Cotización Venezuela → Brasil":

        clientes[chat_id] = {
            "etapa": "menu",
            "direcao": "venezuela_brasil"
        }

        enviar_mensagem(
            chat_id,
            "🇻🇪➡️🇧🇷 *Venezuela → Brasil*\n\n"
            "Selecciona el tipo de cotización:",
            teclado_venezuela_brasil()
        )

        return True

    if texto == "💵 Equivalente en Dólares BCV a convertir en Reais":
        pedir_valor(chat_id, 4)

        return True

    if texto == "🇻🇪 Bolívares a enviar desde Vzla":

        pedir_valor(chat_id, 5)

        return True

    if texto == "🇧🇷 Reais a recibir en Brasil":

        pedir_valor(chat_id, 6)

        return True

    # --------------------------------------------------------
    # MENSAGEM NÃO RECONHECIDA
    # --------------------------------------------------------

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
