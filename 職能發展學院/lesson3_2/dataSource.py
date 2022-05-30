import requests

AREA = ["文山區","內湖區","南港區","萬華區","大安區","中正區","松山區","信義區","北投區","大同區","士林區","中山區"]
def download():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    if response.status_code == 200:
        print("下載成功")
        youbikeList = response.json()
        return youbikeList

