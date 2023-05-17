#下載"台指期""電子期""金融期"即時資料(一般交易行情) = 上午盤
import requests as r # 下載資料套件
import pandas as pd # 資料處理套件
import datetime as dt
from datetime import date, datetime


def get_realtime_futures_info(futures_id):

    url = "https://mis.taifex.com.tw/futures/api/getQuoteList"

    payload = {"MarketType":"0",
            "SymbolType":"F",
            "KindID":"1",
            "CID":f"{futures_id}",
            "ExpireMonth":"",
            "RowSize":"全部",
            "PageNo":"",
            "SortColumn":"",
            "AscDesc":"A"}
    try:
        res = r.post(url, json = payload)
    except:
        print("連線出錯了")
    #print(res) # 200代表成功
    data = res.json()
    #print(data)
    futures_df = pd.DataFrame(data['RtData']['QuoteList'])
    #print(futures_df)
    futures_df = futures_df[['DispCName', 'CLastPrice','CTime']]

    #重新命名欄位
    futures_df = futures_df.rename(columns={"DispCName": "Product",  "CLastPrice": "Last Price", "CTime": "Time"})
    
    # Convert the 'Time' column of to a DatetimeIndex type
    futures_df['Time'] = pd.to_datetime(futures_df['Time'], format="%H%M%S") #%H%M%S因為原始時間是ex:134500

    # Keep the second row
    futures_df = futures_df.iloc[1:2]

##FF0000取得及時期貨交易時間#FF0000
    today = date.today()# Get today's date
    current_trading_time = futures_df.loc[1, 'Time']
    # Combine today's date with the current trading time
    current_time = datetime.combine(today, current_trading_time.time())

### 把即時股價的時間改成今天的日期年月日，不要有小時分秒 ===
    # get today's date
    today = dt.date.today()
    # set the year, month, and day to today's date
    futures_df['Time'] = pd.to_datetime(futures_df['Time']).apply(lambda x: dt.datetime(year=today.year, month=today.month, day=today.day))
### ===========================================

    # rename the "Time" column to "date"
    futures_df = futures_df.rename(columns={'Time': 'date'})

    # 將資料轉向
    futures_df = futures_df.pivot(index='date', columns='Product', values='Last Price')

    # get the name of the column header
    col_name = futures_df.columns[0]

    # 將期貨名稱改為TX、TE、TF以利和歷史價格合併
    if futures_df.columns.str.contains('臺指').any():
        futures_df.rename(columns={col_name : 'TX'}, inplace=True)
    elif futures_df.columns.str.contains('電子').any():
        futures_df.rename(columns={col_name : 'TE'}, inplace=True)
    elif futures_df.columns.str.contains('金融').any():
        futures_df.rename(columns={col_name : 'TF'}, inplace=True)

    # print(futures_df.columns)
    # #把下載的資料另存成csv檔
    #futures_df.to_csv('RT_futPx.csv')

    return futures_df, current_time

# a, b = get_realtime_futures_info("FXF")
# print(a)
# print(a.columns)
# print(b)