import requests
url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=2330'

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

def get_2330():
    response = requests.get(url,headers=headers)
    if response.status_code == requests.codes.ok:
        response.encoding = "utf-8"
        print(response.text)
    else:
        print("下載失敗")
