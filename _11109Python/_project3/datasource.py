
import requests

def get_forcase_data(cityName,api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={cityName},tw&APPID={api_key}&lang=zh_tw&units=metric"
    response = requests.get(url)
    if response.ok :
        print("下載成功")
        allData = response.json()
        city = allData['city']
        return city