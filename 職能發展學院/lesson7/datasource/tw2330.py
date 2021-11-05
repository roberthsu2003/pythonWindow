import requests
from bs4 import BeautifulSoup
url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=2330'

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

def get_2330():
    response = requests.get(url,headers=headers)
    if response.status_code == requests.codes.ok:
        response.encoding = "utf-8"
        bs = BeautifulSoup(response.text)
        dataList = bs.find('div',attrs={'id':'txtFinDetailData'}).find_all('tr',attrs={'align':'center'})
        allDataList = []
        for trTag in dataList:
            tdList = trTag.find_all('td')
            list1 = [tdTag.string for tdTag in tdList] #comprehension
            allDataList.append(list1)
        print(allDataList)
    else:
        print("下載失敗")
