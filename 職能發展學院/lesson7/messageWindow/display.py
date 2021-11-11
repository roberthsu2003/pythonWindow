import tkinter as tk

columnCount = 8
class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        self.title(stockName)
        self.yearsText = [secondList[0] for secondList in dataList]
        tk.Label(self,text=f'{stockName}歷年經營績效查詢',font=('arial',20)).pack(padx=10,pady=10)
        #建立buttonsFrame
        buttonsFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300,height=80)
        for yearIndex,year in enumerate(self.yearsText):
            rIndex = yearIndex // columnCount  #求得按鈕row的索引編號
            cIndex = yearIndex % columnCount #求得按鈕column的索引編號
            btn = tk.Button(buttonsFrame,text=year)
            btn.grid(row=rIndex,column=cIndex)
            btn.bind("<Button-1>",self.buttonClick)
        #buttonsFrame.pack_propagate(0)
        buttonsFrame.pack(padx=20,pady=20)

        self.infoContainer = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=800,height=80)
        #-----顯示value的內容
        self.displayInfoContent(self.infoContainer,'2011')
        #-----顯示value內容
        self.infoContainer.pack_propagate(0)
        self.infoContainer.pack()

    def displayInfoContent(self,parent,year):
        self.yearLabel = tk.Label(parent, text=year)
        self.yearLabel.pack()
        self.subFrame=tk.Frame(parent)
        titleLabelList = ['年度', '股本(億)', '財報評分', '收盤', '平均', '漲跌', '漲跌(%)', '營業收入',
         '營業毛利', '營業利益', '業外損益', '稅後淨利', '營業毛利', '營業利益', '業外損益',
         '稅後淨利', 'ROE(%)', 'ROA(%)', '稅後EPS', 'EPS年增(元)', 'BPS(元)']
        for labelIndex,labelText in enumerate(titleLabelList):
            rowIndex = labelIndex // 11
            columnIndex = labelIndex % 11
            tk.Label(self.subFrame,text=labelText).grid(row=rowIndex*2 ,column=columnIndex)
        self.subFrame.pack()

    def buttonClick(self,event):
        pressedBtn = event.widget #取得被按按鈕的參考
        print(pressedBtn['text']) #透過參考取得按鈕的文字



