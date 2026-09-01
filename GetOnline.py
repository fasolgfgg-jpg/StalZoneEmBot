import requests
from Config import Config


class Online:

    @staticmethod
    def GetStalCraftOnline():
        # Ключ для этого метода Steam API не обязателен, но при лимитах его стоит задать
        # в .env как STEAM_API_KEY
        steam_key = Config.get("STEAM_API_KEY", default="")
        URL = (
            "https://api.steampowered.com/ISteamUserStats/"
            f"GetNumberOfCurrentPlayers/v1/?appid=1818450&key={steam_key}"
        )
        try:
            response = requests.get(URL)
            data = response.json()
            ConvertData = data['response']['player_count']
            return ConvertData
        except:
            return "Не установлен"
