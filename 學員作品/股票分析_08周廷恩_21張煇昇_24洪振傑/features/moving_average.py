import pandas as pd

def Calculate_Moving_Average(data: pd.DataFrame, window: int = 5) ->pd.DataFrame:
    # 将日期列转换为日期时间格式
    # 按日期排序（如果未排序的话）
    # data = data.sort_values(by='Date')

    # 计算收盘价的移动平均
    data['sma'] = round(data['Close'].rolling(window=window).mean(),4)
    close_mean:pd.Series=data['Close'].astype(float).mean()
    data['sma'] =data['sma'].fillna(round(close_mean,4))


    return data