import tkinter as tk
from tkinter.simpledialog import Dialog

class InfoDisplay(Dialog):

    def __init__(self,parent,title=None,info=None): #自訂的初始化
        self.stockName = title
        self.subFrame = None  # subFrame一開始設None,建立一個Display的屬性subFrame
        if info is not None:
            self.info = info
            self.yearsText = [secondList[0] for secondList in self.info]
        super().__init__(parent,title)

    def body(self,master):
        topFrame=tk.Frame(master)
        leftFrame = tk.Frame(topFrame,bg='#aaaaaa')
        scrollBar = tk.Scrollbar(leftFrame, orient=tk.VERTICAL)
        scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        listbox = tk.Listbox(leftFrame,yscrollcommand=scrollBar.set)
        scrollBar.config(command=listbox.yview)
        for item in self.info:
            listbox.insert(tk.END, item[0])
        listbox.bind("<<ListboxSelect>>",self.onSelect)
        listbox.pack(side=tk.LEFT,fill=tk.Y)

        #leftFrame.pack_propagate(0)
        leftFrame.pack(side=tk.LEFT,fill=tk.Y)
        #topFrame.pack_propagate(0)


        #右邊資料顯示
        self.infoContainer = tk.Frame(topFrame)
        tk.Label(self.infoContainer, text=f'{self.stockName}-歷年經營績效查詢', font=('arial', 20)).pack(padx=10, pady=10)
        # -----顯示value的內容
        self.displayInfoContent(self.infoContainer, self.yearsText[0])
        # -----顯示value內容
        #self.infoContainer.pack_propagate(0)
        self.infoContainer.pack(side=tk.RIGHT,padx=10)


        topFrame.pack(padx=20,pady=20)

        print("master:",master)
        print("傳過來的資料:",self.info)

    def onSelect(self,event):
        widget = event.widget
        index = widget.curselection()[0]
        year = widget.get(index)
        self.displayInfoContent(self.infoContainer,year)

    def displayInfoContent(self,parent,year):
        if self.subFrame:
            self.subFrame.destroy() #如果已經有subFrame,則將subFrame消滅

        self.subFrame=tk.Frame(parent)
        yearindex = self.yearsText.index(year)
        valueList = self.info[yearindex] #儲存value內容
        titleLabelList = ['年度', '股本(億)', '財報評分', '收盤', '平均', '漲跌', '漲跌(%)', '營業收入',
         '營業毛利', '營業利益', '業外損益', '稅後淨利', '營業毛利', '營業利益', '業外損益',
         '稅後淨利', 'ROE(%)', 'ROA(%)', '稅後EPS', 'EPS年增(元)', 'BPS(元)']
        for labelIndex,labelText in enumerate(titleLabelList):
            columnCount = 8 #顯示欄位數量
            rowIndex = labelIndex // columnCount
            columnIndex = labelIndex % columnCount
            tk.Label(self.subFrame,text=labelText,bg='#999999').grid(row=rowIndex*2 ,column=columnIndex,sticky='ew') #title的文字，分2列,0和1
            tk.Label(self.subFrame, text=valueList[labelIndex]).grid(row=(rowIndex * 2)+1, column=columnIndex,sticky='ew')  # value的文字，分2列,1和3
        self.subFrame.pack()



    #def buttonbox(self):
    #    pass

