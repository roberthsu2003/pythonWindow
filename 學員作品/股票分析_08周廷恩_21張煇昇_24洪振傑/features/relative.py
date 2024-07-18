import pandas as pd

def Calculate_Rsi(data:pd.DataFrame, window=14)->pd.DataFrame:
    """
    Calculate RSI (Relative Strength Index) for given data.
    
    Parameters:
    - data: pandas DataFrame with 'Close' prices.
    - window: RSI window period (default is 14).
    
    Returns:
    - pandas Series with RSI values.
    """

    delta = pd.Series(data['Close'].astype(float).values).diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = round(100 - (100 / (1 + rs)),4)
    
    data['rsi']=rsi
    close_mean:pd.Series=data['Close'].astype(float).mean()
    data['rsi']=data['rsi'].fillna(round(close_mean,4))

    return data

