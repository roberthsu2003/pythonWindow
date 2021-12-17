from datasource import getStockInfo
import tkinter as tk

#stockInfo = getStockInfo("2330") #股票資料StockInfo的實體
#print(stockInfo)

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    window = Window()
    window.mainloop()


