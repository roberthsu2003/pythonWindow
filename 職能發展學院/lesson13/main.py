from datasource import getStockInfo,closeDirver
import tkinter as tk
from threading import Timer

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #建立Timer的實體,一開始設為None,未來可以判斷,如果是None,代表目前沒有重覆執行
        self.timer = None

        #-----------建立title----------
        self.title("股票成交價及時查詢系統")
        mainFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=2)
        titleFrame = tk.Frame(mainFrame)
        tk.Label(titleFrame,text="股票成交價及時查詢系統",font=('Arial',20,'bold'),fg='#555555').pack(padx=10)
        titleFrame.pack(pady=30)

        #-------------建立inputFrame--------------
        self.inputFrame = tk.Frame(mainFrame,width=50)
        tk.Label(self.inputFrame,text="輸入欲查詢的股票號碼:",font=('Arial',13)).grid(row=0,column=0,sticky=tk.E)
        self.stockIDEntry = tk.Entry(self.inputFrame,textvariable=tk.StringVar(),bd=5)
        self.stockIDEntry.grid(row=0,column=1,sticky=tk.E)
        submitButton = tk.Button(self.inputFrame,font=("Arial",15),text="搜尋",command=self.getStockID)
        submitButton.grid(row=0,column=2,sticky=tk.E)
        self.inputFrame.pack()


        #-------------建立顯示畫面-----------------
        self.listFrame = tk.Frame(mainFrame)

        tk.Label(self.listFrame,text="公司名",font=("Arial",14)).grid(row=0,column=0,sticky=tk.E,padx=10,pady=10)
        self.titleLabel = tk.Label(self.listFrame,text="",font=("Arial",14))
        self.titleLabel.grid(row=0,column=1,sticky=tk.W,padx=10,pady=10)

        tk.Label(self.listFrame, text="累紀成交量", font=("Arial", 14)).grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)
        self.total_oddLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.total_oddLabel.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="開盤價", font=("Arial", 14)).grid(row=2, column=0, sticky=tk.E, padx=10, pady=10)
        self.openPriceLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.openPriceLabel.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="當日最高", font=("Arial", 14)).grid(row=3, column=0, sticky=tk.E, padx=10, pady=10)
        self.highestLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.highestLabel.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="當日最低", font=("Arial", 14)).grid(row=4, column=0, sticky=tk.E, padx=10, pady=10)
        self.lowestLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.lowestLabel.grid(row=4, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="撮合時間", font=("Arial", 14)).grid(row=5, column=0, sticky=tk.E, padx=10, pady=10)
        self.matchTimeLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.matchTimeLabel.grid(row=5, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="成交價", font=("Arial", 14)).grid(row=6, column=0, sticky=tk.E, padx=10, pady=10)
        self.rightPriceLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.rightPriceLabel.grid(row=6, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="漲跌價差", font=("Arial", 14)).grid(row=7, column=0, sticky=tk.E, padx=10, pady=10)
        self.differentPriceLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.differentPriceLabel.grid(row=7, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="漲跌(百分比)", font=("Arial", 14)).grid(row=8, column=0, sticky=tk.E, padx=10, pady=10)
        self.differentPercentLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.differentPercentLabel.grid(row=8, column=1, sticky=tk.W, padx=10, pady=10)

        tk.Label(self.listFrame, text="成交量", font=("Arial", 14)).grid(row=9, column=0, sticky=tk.E, padx=10,pady=10)
        self.dealCountLabel = tk.Label(self.listFrame, text="", font=("Arial", 14))
        self.dealCountLabel.grid(row=9, column=1, sticky=tk.W, padx=10, pady=10)
        self.listFrame.pack()

        mainFrame.pack(pady=30,padx=30,ipadx=30,ipady=30)

    def getStockID(self):
        print("執行")
        inputID = self.stockIDEntry.get()
        stockInfo = getStockInfo(inputID)  # 股票資料StockInfo的實體
        print(stockInfo)
        self.titleLabel.config(text=stockInfo.title)
        self.total_oddLabel.config(text=stockInfo.total_odd)
        self.openPriceLabel.config(text=stockInfo.openPrice)
        self.highestLabel.config(text=stockInfo.highest)
        self.lowestLabel.config(text=stockInfo.lowest)
        self.matchTimeLabel.config(text=stockInfo.matchTime)
        self.rightPriceLabel.config(text=stockInfo.rightPrice)
        self.differentPriceLabel.config(text=stockInfo.differentPrice)
        self.differentPercentLabel.config(text=stockInfo.differentPercent)
        self.dealCountLabel.config(text=stockInfo.dealCount)

        #第一次執行時,不需要取消執行,第2次執行要取消重覆執行,再建立新的重覆執行(因為按搜尋按鈕多次)
        if self.timer is not None:
            self.timer.cancel() #取消重覆執行
        self.timer=Timer(20,self.getStockID)
        self.timer.start()

def closeWindow():
    """
    關閉應用程式,會執行這個function
    關閉應用程式時,Timer實體要被關閉
    :return: None
    """
    if window.timer is not None and window.timer.is_alive():
        window.timer.cancel()

    closeDirver() #關閉driver
    window.destroy()



if __name__ == "__main__":
    window = Window()
    window.protocol("WM_DELETE_WINDOW",closeWindow)
    window.mainloop()


