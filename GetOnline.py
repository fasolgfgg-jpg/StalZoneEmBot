class Online:

    @staticmethod
    def GetStalCraftOnline():
        import requests
        URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=1818450&key="
        try:
            response = requests.get(URL)
            data = response.json()
            ConvertData = data['response']['player_count']
            return ConvertData
        except:
            return "Не установлен"

#import Debug
#Debug.WriteLine(type='OK', message=f"Актуальный онлайн: {Online.GetStalCraftOnline()}")

