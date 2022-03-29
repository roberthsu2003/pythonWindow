import requests
from bs4 import BeautifulSoup

def download_cathay():
    cathay = 'https://cathaybk.com.tw/cathaybk/personal/deposit-exchange/rate/currency-billboard/'
    response = requests.get(cathay)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.find('table')
    datas = soup.find_all(name='tr',attrs={'class':{'rate_list'}})
    coinlist=[]
    for i in range(len(datas)):
        coin=[]
        for data in datas[i].stripped_strings:
            coin.append(data.replace("\n",'').strip())
        del coin[3:5]
        coinlist.append(coin)
    return coinlist

def download_land():
    land = "https://rate.landbank.com.tw/zh-TW/Foreign?mid=35&btnID=btn01"
    response = requests.get(land)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.find('table')
    datas = soup.find_all(name='tr')
    coinlist=[]
    for i in range(len(datas)):
        coin=[]
        for data in datas[i].stripped_strings:
            coin.append(data.replace("\n",'').strip())
        del coin[5:]
        coinlist.append(coin)
    return coinlist[2:]

def download_taiwan():
    taiwan = 'https://rate.bot.com.tw/xrt/all/day'
    response = requests.get(taiwan)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.find('table')
    datas = soup.find_all(name='tr')
    coinlist = []
    for i in range(len(datas)):
        coin = []
        for data in datas[i].stripped_strings:
            coin.append(data.replace("\n", '').strip())
        del coin[:1]
        del coin[5:]
        coinlist.append(coin)
    return coinlist[2:]

def download_citi():
    citi = 'https://www.citibank.com.tw/TWGCB/APBAASDP/fxrts/flow.action?TTC=29&selectedBCC=TWD'
    response = requests.get(citi)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.find('table')
    datas = soup.find_all(name='tr')
    coinlist = []
    for i in range(len(datas)):
        coin = []
        for data in datas[i].stripped_strings:
            coin.append(data.replace("\n", '').strip())
        coinlist.append(coin)
        del coinlist[46:]
    return coinlist[32:]

def download_esun():
    esun = 'https://www.esunbank.com.tw/bank/personal/deposit/rate/forex/foreign-exchange-rates'
    response = requests.get(esun)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.find('table')
    datas = soup.find_all(name='tr')
    coinlist = []
    for i in range(len(datas)):
        coin = []
        for data in datas[i].stripped_strings:
            coin.append(data.replace("\n", '').strip())
        del coin[3:5]
        coinlist.append(coin)
    for i in range(len(coinlist[2:])):
        if len(coinlist[2:][i]) < 5:
            coinlist[2:][i].append('--')
            coinlist[2:][i].append('--')
    return coinlist[2:]
