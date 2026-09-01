import requests
import Debug
import json

class Tool:
    @staticmethod
    def reader():
        with open("keys.json", "r") as f:
            data = json.load(f)
        TOKEN = data["TG-Client-Token"]
        return TOKEN

    @staticmethod
    def EmissionCheck():
        url = "https://eapi.stalcraft.net/RU/emission"

        with open("keys.json", "r") as f:
            data = json.load(f)

        headers = {
        "Content-Type": "application/json",
        "Client-Secret": data["Client-Secret"],
        "Client-ID": data["Client-ID"],
        }

        response = requests.get(url, headers=headers)
        Debug.WriteLine("Info", response.text)
        return response
    #print(response.text)
#EmissionCheck()