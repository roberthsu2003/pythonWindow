import tkinter as tk

columnCount = 8
class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        self.dataList = dataList
        self.subFrame = None #subFrame一開始設None,建立一個Display的屬性subFrame
        self.title(stockName)
        self.yearsText = [secondList[0] for secondList in dataList]
        tk.Label(self,text=f'{stockName}-歷年經營績效查詢',font=('arial',20)).pack(padx=10,pady=10)
        #建立buttonsFrame
        buttonsFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300,height=80)
        for yearIndex,year in enumerate(self.yearsText):
            rIndex = yearIndex // columnCount  #求得按鈕row的索引編號
            cIndex = yearIndex % columnCount #求得按鈕column的索引編號
            btn = tk.Button(buttonsFrame,text=year,padx=5,pady=5)
            btn.grid(row=rIndex,column=cIndex)
            btn.bind("<Button-1>",self.buttonClick)
        #buttonsFrame.pack_propagate(0)
        buttonsFrame.pack(padx=20,pady=20)

        self.infoContainer = tk.Frame(self,width=800,height=150)
        #-----顯示value的內容
        self.displayInfoContent(self.infoContainer,self.yearsText[0])
        #-----顯示value內容
        self.infoContainer.pack_propagate(0)
        self.infoContainer.pack()

        tk.Button(self,text="關閉視窗",font=('arial',16),padx=10,pady=10,command=self.windowclose).pack(padx=50,pady=20)

    def displayInfoContent(self,parent,year):
        if self.subFrame:
            self.subFrame.destroy() #如果已經有subFrame,則將subFrame消滅

        self.subFrame=tk.Frame(parent)
        yearindex = self.yearsText.index(year)
        valueList = self.dataList[yearindex] #儲存value內容
        titleLabelList = ['年度', '股本(億)', '財報評分', '收盤', '平均', '漲跌', '漲跌(%)', '營業收入',
         '營業毛利', '營業利益', '業外損益', '稅後淨利', '營業毛利', '營業利益', '業外損益',
         '稅後淨利', 'ROE(%)', 'ROA(%)', '稅後EPS', 'EPS年增(元)', 'BPS(元)']
        for labelIndex,labelText in enumerate(titleLabelList):
            rowIndex = labelIndex // 11
            columnIndex = labelIndex % 11
            tk.Label(self.subFrame,text=labelText,bg='#999999').grid(row=rowIndex*2 ,column=columnIndex,sticky='ew') #title的文字，分2列,0和1
            tk.Label(self.subFrame, text=valueList[labelIndex]).grid(row=(rowIndex * 2)+1, column=columnIndex,sticky='ew')  # value的文字，分2列,1和3
        self.subFrame.pack()

    def buttonClick(self,event):
        pressedBtn = event.widget #取得被按按鈕的參考
        year = pressedBtn['text'] #透過參考取得按鈕的文字
        self.displayInfoContent(self.infoContainer, year)

    def windowclose(self):
        self.destroy()


