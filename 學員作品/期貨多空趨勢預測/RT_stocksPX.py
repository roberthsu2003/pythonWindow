#下載"股票"即時資料
import twstock
import pandas as pd


def get_realtime_stock_info(stock_codes): #stock_codes is a list of stock codes
    stock_multi = twstock.realtime.get(stock_codes) 
    stock_df = pd.DataFrame()

    for stock in stock_codes:
        df_ = pd.DataFrame(stock_multi[stock])
        stock_info = df_.iloc[0:5, 1]
        stock_realtime = df_.iloc[5:, 2]
        stock_data = pd.concat([stock_info, stock_realtime], ignore_index=True)
        df_['data'] = list(stock_data)
        df_ = df_.drop(['timestamp', 'info', 'realtime', 'success'], axis=1)
        df_ = df_.T
        stock_df = pd.concat([stock_df, df_], ignore_index=True)
    
    stock_df.columns = ['股票代碼', '股票代碼全', '股票名稱', '公司名','下載時間', '最新成交價', '成交量', '累計成交量', '最佳5檔賣出價', '最佳5檔賣出量', '最佳5檔買進價', '最佳5檔買進量', '開盤價', '最高價', '最低價']

    #選取需要的欄位
    stock_df = stock_df.loc[:, ['股票代碼', '下載時間', '最新成交價']]

    column_names = {
        '股票代碼': 'Stock Code',
        '下載時間': 'Date',
        '最新成交價': 'Last Price'
    } #下載時間叫Date是為了和歷史股價合併放在同一個csv

    # Rename the columns using the dictionary
    stock_df = stock_df.rename(columns=column_names)

    # Pivot the dataframe
    stock_df = stock_df.pivot(index='Date', columns='Stock Code', values='Last Price')

    # 確認股票順序是輸入順序Reorder the columns based on the original list of stock codes
    stock_df = stock_df.reindex(columns=stock_codes)

    #stock_df.to_csv('realtime.csv')

    return stock_df

stock_codes =[2330, 2317, 2454]
a = get_realtime_stock_info(stock_codes)
a.to_csv('a.csv')