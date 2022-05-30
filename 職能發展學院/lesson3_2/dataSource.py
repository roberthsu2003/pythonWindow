import requests

def download():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    if response.status_code == 200:
        print("下載成功")
        youbikeList = response.json()
        return youbikeList

