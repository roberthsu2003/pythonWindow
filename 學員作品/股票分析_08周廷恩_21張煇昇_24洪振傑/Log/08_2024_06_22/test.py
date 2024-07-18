import pandas as pd
import numpy as np
import yfinance as yf


# 下載股票數據
ticker = 'AAPL'  # 這裡使用蘋果公司（AAPL）作為例子
start_date = '2008-01-01'
end_date = '2023-12-31'
data = yf.download(ticker, start=start_date, end=end_date)

# 計算MACD指標的函數
def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA12'] = df['Close'].ewm(span=short_window, min_periods=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, min_periods=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, min_periods=signal_window, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    return df

# 調用計算MACD指標的函數
data = calculate_macd(data)

# 打印出計算後的數據，這裡只打印最後幾行
print(data[['Close', 'EMA12', 'EMA26', 'MACD', 'Signal_Line', 'MACD_Histogram']].tail(20))

data.to_csv('stocks.csv', index=False)
