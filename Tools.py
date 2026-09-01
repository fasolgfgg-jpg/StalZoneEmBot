import requests
import Debug
from Config import Config


class Tool:
    @staticmethod
    def token():
        """Токен Telegram-бота (переменная окружения TG_CLIENT_TOKEN)."""
        return Config.get("TG_CLIENT_TOKEN")

    @staticmethod
    def EmissionCheck():
        url = "https://eapi.stalcraft.net/RU/emission"

        headers = {
            "Content-Type": "application/json",
            "Client-Secret": Config.get("CLIENT_SECRET"),
            "Client-ID": Config.get("CLIENT_ID"),
        }

        response = requests.get(url, headers=headers)
        Debug.WriteLine("Info", response.text)
        return response
