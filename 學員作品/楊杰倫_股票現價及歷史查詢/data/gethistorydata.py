import requests
import json
from bs4 import BeautifulSoup

def get_history_data(odd_number):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

    response = requests.get(f'https://histock.tw/stock/chips.aspx?no={odd_number}',headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        html_data = soup.find('div', {'class': 'row-stock w1060'}).find("script").string
    except:
        return None

    data_dic = {}

    data_dic["外資"] = get_data(html_data, "外資")
    data_dic["投信"] = get_data(html_data, "投信")
    data_dic["自營商"] = get_data(html_data, "自營商")
    data_dic["三大法人"] = get_data(html_data, "三大法人")
    data_dic["外資持股率"] = get_data3(html_data, "name: '外資持股率(%)'")
    data_dic["股價"] = get_data2(html_data, "'candlestick'")

    '''嘗試讀取本地資料，若無則寫新的'''
    try:
        history_data = read_history_data()
        with open("history.json", "w", encoding="utf-8") as f:
            history_data[odd_number] = data_dic

            json.dump(history_data, f, ensure_ascii=False)
        return history_data

    except:
        with open("history.json", "w", encoding="utf-8") as f:
            data_dic_top = {}
            data_dic_top[odd_number] =data_dic

            json.dump(data_dic_top, f, ensure_ascii=False)

        return data_dic_top

def get_data(a,name):
    '''清洗資料，轉成list格式的資料，用於外資、投信、自營商、三大法人'''
    if a[a.find(name):] == -1:
        return None
    b = a[a.find(name):]
    c = b[b.find("threeData"):]
    f = c[c.find("[")+2:c.find(";")-3]

    h = f.replace("],[",",")
    i = h.split(",")

    return i

def get_data2(a,name):
    '''清洗資料，轉成list格式的資料，用於股價'''
    b = a[a.find(name):]
    c = b[b.find("data"):]
    f = c[c.find("[") + 2:c.find("y") - 17]

    h = f.replace("],[", ",")
    i = h.split(",")

    return i

def get_data3(a,name):
    '''清洗資料，轉成list格式的資料，用於外資持股率'''
    b = a[a.find(name):]
    c = b[b.find("data"):]
    f = c[c.find("[") + 2:c.find("y") - 14]

    h = f.replace("],[", ",")
    i = h.split(",")

    return i

def read_history_data():
    '''讀檔'''
    with open("history.json", "r", encoding="utf-8") as f:
        a = json.loads(f.read())
        return a