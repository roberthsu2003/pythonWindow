from pydantic import BaseModel,RootModel,Field
from datetime import datetime

class StockData(BaseModel):
    date:datetime=Field(alias="日期")
    trading_volume:str=Field(alias="成交股數")
    turnover:str=Field(alias="成交金額")
    open_price:float=Field(alias="開盤價")
    high_price:float=Field(alias="最高價")
    low_price:float=Field(alias="最低價")
    close_price:float=Field(alias="收盤價")
    change:float=Field(alias="漲跌價差")
    transactions:str=Field(alias="成交筆數")

class Data(RootModel):
    root:list[StockData]

def parse_custom_date(date_str):
    year = int(date_str[:3]) + 1911  # 将 "113" 转换为四位数的年份
    month = int(date_str[4:6])       # 月份
    day = int(date_str[7:9])         # 日
    
    return datetime(year, month, day)