import requests
from lxml import etree
from datetime import datetime
import json

def getStockInfo(odd_number=2330,offline_mode=False):
    if offline_mode:
        try:
            a = readjson()
            stockinfo = a[odd_number]
        except:
            pass
    else:
        stockinfo = {}
        best5 = []
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

        try:
            response = requests.get(f'https://invest.cnyes.com/twstock/TWS/{odd_number}',headers=headers)
            content = response.content.decode()
            html = etree.HTML(content)
            element = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[2]/div[1]/div[2]/time")
            print(element[0].text)
            b = str(int(element[0].text[-5:-3]) + 8)
            c = element[0].text[0:-5] + b + element[0].text[-3:]
            stockinfo["資料時間"] = c

            try:
                '''因為這個網站很X，會故意給隨機3分鐘內的資料，因此比對新舊資料，留下較新的資料'''
                a = readjson()
                stockinfo_data_time = a[odd_number]["資料時間"]

                if compare_time(c,stockinfo_data_time) is False:
                    print("選擇留下舊資料")
                    return a[odd_number]
                print("選擇下載資料")
                '''因為這個網站很X，會故意給隨機3分鐘內的資料，因此比對新舊資料，留下較新的資料'''
            except:
                pass

        except Exception as e:
            print(e)
            try:
                a = readjson()
                print("發生例外，讀取舊資料")
                stockinfo = a[odd_number]

                return stockinfo
            except:
                print("發生例外，連線和讀取舊資料都失敗")
                return False

        element = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[1]/div[1]/div/h1/div[1]")
        element2 = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[1]/div[2]")
        '''篩選掉英文的部分'''
        a = element2[0].text.find(" ")
        '''篩選掉英文的部分'''
        newstring = element2[0].text[:a]

        stockinfo["股票名稱"] = element[0].text+" "+newstring

        element = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[2]/div[1]/div[3]/div[1]/div/span")
        stockinfo["價格"] = element[0].text


        element = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]/span")
        element2 = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[2]/span")
        stockinfo["漲跌"] = f"{element[0].text:8s}   {element2[0].text:7s}"

        element = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]")
        stockinfo["成交量"] = element[0].text

        element = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[5]/div[2]")
        stockinfo["開盤價"] = element[0].text

        element = html.xpath("/html/body/div[1]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]")
        middle_index = element[0].text.find("-")

        stockinfo["當日最高"] = element[0].text[middle_index+2:]
        stockinfo["當日最低"] = element[0].text[0:middle_index-1]

        for i in range(5):
            element = html.xpath(
                f"/html/body/div[1]/div/div[3]/div[3]/section[1]/section[1]/div[2]/div[2]/div[1]/div[{1+i}]/div[2]")
            best5.append(element[0].text)
            element = html.xpath(
                f"/html/body/div[1]/div/div[3]/div[3]/section[1]/section[1]/div[2]/div[2]/div[1]/div[{1+i}]/div[1]")
            best5.append(element[0].text)
            element = html.xpath(
                f"/html/body/div[1]/div/div[3]/div[3]/section[1]/section[1]/div[2]/div[2]/div[2]/div[{1+i}]/div[1]")
            best5.append(element[0].text)
            element = html.xpath(
                f"/html/body/div[1]/div/div[3]/div[3]/section[1]/section[1]/div[2]/div[2]/div[2]/div[{1+i}]/div[2]")
            best5.append(element[0].text)

        try:
            a = readjson()
            with open("stockInfo.json", "w", encoding="utf-8") as f:
                stockinfo["五檔報價"] = best5
                a[odd_number] = stockinfo
                json.dump(a, f, ensure_ascii=False)
        except:
            with open("stockInfo.json", "w", encoding="utf-8") as f:
                a = {}
                stockinfo["五檔報價"] = best5
                a[odd_number]= stockinfo
                json.dump(a, f, ensure_ascii=False)

    return stockinfo

def readjson():
    with open("stockInfo.json", "r", encoding="utf-8") as f:
        a = json.loads(f.read())

    return a

def compare_time(a_time,b_time):
    if trans_time(a_time)>=trans_time(b_time):
        return True
    else:
        return False

def trans_time(time):
    year = int(datetime.now().strftime('%Y'))
    month = int(datetime.strptime(time, "%m/%d %H:%M").strftime("%m"))
    day = int(datetime.strptime(time, "%m/%d %H:%M").strftime("%d"))
    hour = int(datetime.strptime(time, "%m/%d %H:%M").strftime("%H"))
    min = int(datetime.strptime(time, "%m/%d %H:%M").strftime("%M"))

    return datetime(year, month, day, hour, min).timestamp()