import os
import requests
import time
import json


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def enviar_mensagem(chat_id, texto, teclado=None):
    dados = {
        "chat_id": chat_id,
        "text": texto
    }

    if teclado:
        dados["reply_markup"] = json.dumps(teclado)

    requests.post(
        f"{BASE_URL}/sendMessage",
        data=dados
    )


def main():
    offset = None

    print("MiguelFM iniciado. Aguardando mensagens...")

    while True:
        resposta = requests.get(
            f"{BASE_URL}/getUpdates",
            params={
                "offset": offset,
                "timeout": 30
            }
        )

        dados = resposta.json()

        for atualizacao in dados.get("result", []):
            offset = atualizacao["update_id"] + 1

            mensagem = atualizacao.get("message")

            if not mensagem:
                continue

            chat_id = mensagem["chat"]["id"]
            texto = mensagem.get("text", "")

            if texto == "/start":
                teclado = {
                    "keyboard": [
                        [{"text": "🇧🇷➡️🇻🇪 Cotización Brasil → Venezuela"}],
                        [{"text": "🇻🇪➡️🇧🇷 Cotización Venezuela → Brasil"}],
                        [{"text": "👤 Hablar directamente con Miguel"}]
                    ],
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                }

                enviar_mensagem(
                    chat_id,
                    "¡Hola! 👋 Bienvenido a MiguelFM.\n\n"
                    "¿Qué deseas hacer?",
                    teclado
                )


if __name__ == "__main__":
    main()
