import os
import requests


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("A variável TELEGRAM_BOT_TOKEN não foi configurada.")


def main():
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"

    response = requests.get(url)
    data = response.json()

    print(data)


if __name__ == "__main__":
    main()
