from datasource import getStockInfo

stockInfo = getStockInfo("2330") #股票資料StockInfo的實體
print(stockInfo.title)
print(stockInfo.highest)


