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
        mainFrame.pack()

    def getStockID(self):
        print("getStockID")

if __name__ == "__main__":
    window = Window()
    window.mainloop()


