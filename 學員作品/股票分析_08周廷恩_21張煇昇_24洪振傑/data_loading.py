import os
import requests
import datetime as dt # 時間套件
import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta

def Check_Data_Csv():
    if os.path.exists("data.csv"):
        print("檔案存在")
        return True
    else:
        return False

def Get_N_Month_Data(stock_id:int,start_year:str, start_month:str, end_year:str, end_month:str) ->pd.DataFrame:
    ticker = f'{stock_id}.TW'
    start_date = f'{start_year}-{start_month}-01'
    end_date = pd.to_datetime(f'{end_year}-{end_month}-01') + pd.offsets.MonthEnd(0)
    end_date = end_date.strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()

    return data
    
def Get_Data_Dict(data:pd.DataFrame)->dict:
    
    try:
        if not data.empty: 
            columns_list = data.columns.tolist()
            datas_list = data.values.tolist()

            final_dict_list = []
            for row in datas_list:
                row_dict = {columns_list[i]: row[i] for i in range(len(columns_list))}
                final_dict_list.append(row_dict)
        
            return final_dict_list
        else:
            print("資料遺失或空白 DataFrame")
            return {}
    except Exception as e:
        print(f"發生錯誤: {str(e)}")
        return {}
    

    
