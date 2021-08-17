#!/usr/bin/python3
'''
輸入股票代號即時查詢股票資料
並設置提醒功能在高於或低於設定金額時
跳出視窗提醒使用者
讓使用者不需要時常看著視窗
'''

from tkinter import *
from tkinter import messagebox
from threading import Timer
import DataSourse
import time

class Stock(Tk):
    def __init__(self):
        super().__init__()
        # 建立視窗
        self.title("股票成交價及時查詢提醒系統")
        self.resizable(width=0, height=0)
        # =============建立mainFrame==============
        # 主區塊
        mainFrame = Frame(self, relief="groove", borderwidth=2)

        # -------------建立titleFrame-------------
        # 標題區塊
        titleFrame = Frame(mainFrame)
        Label(titleFrame, text='股票成交價及時查詢提醒系統', font=("Arial", 20, 'bold'), fg='#555555').pack(padx=10)
        titleFrame.pack(fill=X)
        # -------------titleFrame顯示-------------

        Label(mainFrame, text="---------------------------").pack() # 分隔線

        # -------------建立inputFrame-------------
        # 輸入區塊
        self.inputFrame = Frame(mainFrame,width=50)

        Label(self.inputFrame, text="輸入欲查詢的股票號碼: ",font=("Arial",13)).grid(row=0 , column=0, sticky=E)
        self.stockID = Entry(self.inputFrame,textvariable=StringVar(), bd=5)
        self.stockID.grid(row=0 , column=1, sticky=E)
        dataButton = Button(self.inputFrame,font=("Arial",15),text="搜尋",command=self.getStockID)
        dataButton.grid(row=0 , column=2, sticky=E)

        self.inputFrame.pack()
        # -------------inputFrame顯示-------------

        # -------------建立list Frame-------------
        # 顯示內容區塊
        self.listFrame = Frame(mainFrame)

        Label(self.listFrame, text='公司名:', font=("Arial", 14)).grid(row=0, column=0, sticky=E, padx=10, pady=10)
        self.companyLabel = Label(self.listFrame, text="", font=("Arial", 14))
        self.companyLabel.grid(row=0, column=1, sticky=W, padx=10, pady=10)

        Label(self.listFrame, text='目前成交價:', font=("Arial", 14)).grid(row=1, column=0, sticky=E, padx=10, pady=10)
        self.closeLabel = Label(self.listFrame, text="", font=("Arial", 14))
        self.closeLabel.grid(row=1, column=1, sticky=W, padx=10, pady=10)

        Label(self.listFrame, text='最高成交價:', font=("Arial", 14)).grid(row=2, column=0, sticky=E, padx=10, pady=10)
        self.highLabel = Label(self.listFrame, text="", font=("Arial", 14))
        self.highLabel.grid(row=2, column=1, sticky=W, padx=10, pady=10)

        Label(self.listFrame, text='最低成交價:', font=("Arial", 14)).grid(row=3, column=0, sticky=E, padx=10, pady=10)
        self.lowLabel = Label(self.listFrame, text="", font=("Arial", 14))
        self.lowLabel.grid(row=3, column=1, sticky=W, padx=10, pady=10)

        Label(self.listFrame, text='開盤價:', font=("Arial", 14)).grid(row=4, column=0, sticky=E, padx=10, pady=10)
        self.openLabel = Label(self.listFrame, text="", font=("Arial", 14))
        self.openLabel.grid(row=4, column=1, sticky=W, padx=10, pady=10)

        # 提醒金額-高
        self.warnHighPrice = Label(self.listFrame, text="", font=("Arial", 18),fg="#FF0000")
        self.warnHighPrice.grid(row=5, column=1, sticky=W, padx=10, pady=10)
        # 提醒金額-低
        self.warnLowPrice = Label(self.listFrame, text="", font=("Arial", 18),fg="#00DB00")
        self.warnLowPrice.grid(row=6, column=1, sticky=W, padx=10, pady=10)


        # -------------建立warn Frame-------------
        # 提醒區塊
        self.warnFrame = Frame(mainFrame)

        # 提醒按鈕
        self.warnButton = Button(self.warnFrame, text="設定提醒", font=("Arial", 15), command=self.warnWindow)

        # 時間倒數
        self.timeCountLabel = Label(self.warnFrame, text="", font=("Arial", 18))
        self.timeCountLabel.pack()

        mainFrame.pack(pady=30,ipadx=20,ipady=20)
        # =============mainFrame顯示=============


    # 取得資料
    def getStockID(self):
        inputID = self.stockID.get()
        stockName = DataSourse.getName(inputID)
        self.stockData = DataSourse.getData(inputID)

        # 判斷輸入是否正常 不正常就回傳None
        if stockName is None or self.stockData is None:
            messagebox.showinfo("提示訊息", "輸入錯誤!")
        else:
            self.inputFrame.pack_forget() # 輸入欄位移除
            self.listFrame.pack(fill=X) # 資料欄位顯示
            self.warnFrame.pack(fill=X) # 提醒資料欄位顯示

            # 資料內容修改
            self.companyLabel.configure(text=stockName)
            self.closeLabel.configure(text=str(self.stockData['目前成交價'])+" 元")
            self.highLabel.configure(text=str(self.stockData['最高成交價'])+" 元")
            self.lowLabel.configure(text=str(self.stockData['最低成交價'])+" 元")
            self.openLabel.configure(text=str(self.stockData['開盤價'])+" 元")

            # 設置提醒按鈕顯示
            self.warnButton.pack()

    # 提醒視窗
    def warnWindow(self):
        self.warnCheck = Toplevel(self)
        self.warnCheck.title("提醒視窗")
        fontStyle = {'font': ('arial', 13)}

        Label(self.warnCheck, text="請輸入高於多少時提醒: ", **fontStyle).grid(row=0, column=0)
        self.checkHighPriceInput = Entry(self.warnCheck, textvariable=StringVar(), bd=5)
        self.checkHighPriceInput.grid(row=0, column=1)

        Label(self.warnCheck, text="請輸入低於多少時提醒: ", **fontStyle).grid(row=1, column=0)
        self.checkLowPriceInput = Entry(self.warnCheck, textvariable=StringVar(), bd=5)
        self.checkLowPriceInput.grid(row=1, column=1)

        dataButton = Button(self.warnCheck, font=("Arial", 13), text="設置", command=self.setPriceInMain)
        dataButton.grid(row=1, column=3)




    # 設置提醒金額到主視窗
    def setPriceInMain(self):
        self.highPrice = self.checkHighPriceInput.get()
        self.lowPrice = self.checkLowPriceInput.get()

        # 判斷輸入的內容是否數字
        if self.highPrice.isdigit() == False or self.lowPrice.isdigit() == False:
            messagebox.showinfo("提示訊息", "輸入錯誤!")
        else:
            self.warnHighPrice.configure(text=f"成交價超過 {self.highPrice} 元時提醒 ")
            self.warnLowPrice.configure(text=f"成交價低於 {self.lowPrice} 元時提醒 ")
            self.warnButton.pack_forget() # 設置提醒按鈕移除
            self.repeatCheck() # 執行定時更新
            try:
                self.timeCount() # 執行更新倒數
            except:
                pass
            self.warnCheck.destroy() # 設置提醒視窗移除

    # 定時更新
    def repeatCheck(self):
        print("內容更新")
        # 更新內容
        self.closeLabel.configure(text=str(self.stockData['目前成交價']) + " 元")
        self.highLabel.configure(text=str(self.stockData['最高成交價']) + " 元")
        self.lowLabel.configure(text=str(self.stockData['最低成交價']) + " 元")
        # 判斷是否需要提醒
        if float(self.stockData['目前成交價']) >= float(self.highPrice):
            messagebox.showinfo("提示訊息", f"目前成交價 {self.stockData['目前成交價']} 已經高於你設定的金額 {self.highPrice} !")
        elif float(self.stockData['目前成交價']) <= float(self.lowPrice):
            messagebox.showinfo("提示訊息", f"目前成交價 {self.stockData['目前成交價']} 已經低於你設定的金額 {self.highPrice} !")
        else:
            self.nextTime = int(time.time()) + 60
            self.t = Timer(60, self.repeatCheck)
            self.t.start()

    # 更新倒數
    def timeCount(self):
        countTime = self.nextTime - int(time.time())
        self.timeCountLabel.configure(text=f"提醒功能已設置 請不要關閉視窗 剩餘 {countTime} 秒後更新")
        self.timeCountDown = Timer(1,self.timeCount)
        self.timeCountDown.start()

def closeWindow():
    window.destroy()
    try: # 防止沒設提醒就關閉視窗而導致出錯
        window.timeCountDown.cancel()
        window.t.cancel()
    except:
        pass


if __name__ == '__main__':
    window = Stock()
    window.protocol("WM_DELETE_WINDOW", closeWindow)
    window.mainloop()