from datasource import getStockInfo
import tkinter as tk

#stockInfo = getStockInfo("2330") #股票資料StockInfo的實體
#print(stockInfo)

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

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
        inputID = self.stockIDEntry.get()
        stockInfo = getStockInfo(inputID)  # 股票資料StockInfo的實體
        print(stockInfo)

if __name__ == "__main__":
    window = Window()
    window.mainloop()


