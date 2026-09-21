import os
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen


from telegram_bot.bot import processar_mensagem


PORT = int(os.environ.get("PORT", "8080"))

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("TELEGRAM_WEBHOOK_SECRET")
WEBHOOK_URL = os.environ.get("TELEGRAM_WEBHOOK_URL")


class TelegramWebhookHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/health":

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            resposta = {
                "status": "ok",
                "service": "RemitFlow Telegram Webhook"
            }

            self.wfile.write(
                json.dumps(resposta).encode("utf-8")
            )

            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):

        if self.path != "/telegram/webhook":

            self.send_response(404)
            self.end_headers()
            return

        if WEBHOOK_SECRET:

            secret_recebido = self.headers.get(
                "X-Telegram-Bot-Api-Secret-Token"
            )

            if secret_recebido != WEBHOOK_SECRET:

                self.send_response(403)
                self.end_headers()
                return

        try:

            tamanho = int(
                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )

            corpo = self.rfile.read(tamanho)

            atualizacao = json.loads(
                corpo.decode("utf-8")
            )

            mensagem = atualizacao.get("message")

            if mensagem:

                chat = mensagem.get("chat", {})
                chat_id = chat.get("id")

                texto = mensagem.get("text")

                if chat_id and texto:

                    print(
                        f"Mensagem recebida de {chat_id}: {texto}"
                    )

                    processar_mensagem(
                        chat_id,
                        texto
                    )

            self.send_response(200)
            self.end_headers()

            self.wfile.write(b"OK")

        except Exception as erro:

            print("\nERRO AO PROCESSAR WEBHOOK:")
            print(erro)

            self.send_response(500)
            self.end_headers()

    def log_message(self, formato, *args):

        print(
            f"[WEBHOOK] {formato % args}"
        )


def registrar_webhook():

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN não configurado."
        )

    if not WEBHOOK_URL:
        raise RuntimeError(
            "TELEGRAM_WEBHOOK_URL não configurado."
        )

    if not WEBHOOK_SECRET:
        raise RuntimeError(
            "TELEGRAM_WEBHOOK_SECRET não configurado."
        )

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    )

    dados = {
        "url": WEBHOOK_URL,
        "secret_token": WEBHOOK_SECRET
    }

    corpo = json.dumps(dados).encode("utf-8")

    requisicao = Request(
        url,
        data=corpo,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urlopen(requisicao, timeout=30) as resposta:

        resultado = json.loads(
            resposta.read().decode("utf-8")
        )

    if not resultado.get("ok"):

        raise RuntimeError(
            f"Telegram recusou o webhook: {resultado}"
        )

    print(
        "\nWebhook do Telegram registrado com sucesso."
    )

    print(
        f"URL: {WEBHOOK_URL}"
    )


def main():

    print(
        "Iniciando RemitFlow Telegram Webhook..."
    )

    registrar_webhook()

    servidor = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        TelegramWebhookHandler
    )

    print(
        f"Servidor iniciado na porta {PORT}"
    )

    servidor.serve_forever()


if __name__ == "__main__":
    main()
