import pandas as pd
import numpy as np

# 計算MACD指標的函數
def Calculate_Macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA12'] = df['Close'].ewm(span=short_window, min_periods=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, min_periods=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, min_periods=signal_window, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    
    return df

