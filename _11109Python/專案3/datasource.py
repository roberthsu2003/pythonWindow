import requests

api_key = "29c4f184354b9889e87f7b494ac86aed"
cityName = "Taipei"

def get_forcast_data():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={cityName},tw&APPID={api_key}&lang=zh_tw&units=metric"

    response = requests.get(url=url)
    if response.ok:
        print("下載成功")
        return response.json()
    else:
        print("下載失敗")