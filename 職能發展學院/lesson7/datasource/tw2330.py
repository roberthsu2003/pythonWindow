import requests
url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=2330'

def get_2330():
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = "utf-8"
        print(response.text)
    else:
        print("下載失敗")
