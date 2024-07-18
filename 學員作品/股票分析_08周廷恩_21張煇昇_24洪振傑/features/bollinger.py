import pandas as pd

def Calculate_Bollinger_Bands(data: pd.DataFrame, window=20, num_std=2)->pd.DataFrame:
    #計算移動平均線
    data['ma'] = round(data['Close'].rolling(window=window).mean(),4)
    # 計算標準差
    data['std_dev'] = round(data['Close'].rolling(window=window).std(),4)
    
    # 計算布林通道的上限線和下限線
    data['upperband'] = round(data['ma'] + num_std * data['std_dev'],4)
    data['lowerband'] = round(data['ma'] - num_std * data['std_dev'],4)

    return data
