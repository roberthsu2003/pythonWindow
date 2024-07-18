import pandas as pd
from .moving_average import Calculate_Moving_Average
from .relative import Calculate_Rsi
from .bollinger import Calculate_Bollinger_Bands
from .macd import Calculate_Macd


class Feature():
    def __init__(self) :
        self._Calculate_Moving_Average =Calculate_Moving_Average
        self._Calculate_Rsi =Calculate_Rsi
        self._Calculate_Bollinger_Bands =Calculate_Bollinger_Bands
        self._Calculate_Macd=Calculate_Macd

    @property
    def Calculate_Moving_Average(self):
        return self._Calculate_Moving_Average
    @property
    def Calculate_Rsi(self):
        return self._Calculate_Rsi
    @property
    def Calculate_Bollinger_Bands(self):
        return self._Calculate_Bollinger_Bands
    @property
    def Calculate_Macd(self):
        return self._Calculate_Bollinger_Bands