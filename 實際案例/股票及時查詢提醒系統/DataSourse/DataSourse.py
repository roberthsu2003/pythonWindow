import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

# 取得資料
def getData(ID):
    # 檢查輸入的內容是否數字
    if ID.isdigit():
        resData = requests.get("https://www.wantgoo.com/investrue/"+ID+"/daily-candlestick",  headers=headers)
        oldDataDic = resData.json()
    else:
        return None

    # 檢查輸入的數字是否正確
    try:
        newDataDic = {}
        newDataDic['目前成交價'] = oldDataDic['close']
        newDataDic['最高成交價'] = oldDataDic['high']
        newDataDic['最低成交價'] = oldDataDic['low']
        newDataDic['開盤價'] = oldDataDic['open']
    except:
        return None
    else:
        return newDataDic

# 取得名字
def getName(ID):
    try:
        nameData = requests.get("https://www.wantgoo.com/stock/"+ID+"/company-profile-data", headers=headers)
        name = nameData.json()["name"]
    except:
        return None
    else:
        return name


__all__ = ["getData", "getName"]
