import tkinter as tk
from tkinter.simpledialog import Dialog

#自訂Dialog
class ShowInfo(Dialog):
    def __init__(self,parent,title=None,info=None):
        self.info = info
        self.stackname = title
        self.yearsText = [secondList[0] for secondList in self.info]
        super().__init__(parent,title)


    def body(self,master): #override
        self.topFrame = tk.Frame(self) #最外面的frame
        self.subFrame = None  # subFrame一開始設None,建立一個Display的屬性subFrame
        leftFrame = tk.Frame(self.topFrame)
        scrollBar = tk.Scrollbar(leftFrame,orient="vertical")
        self.list = tk.Listbox(leftFrame, width=10, height=10, yscrollcommand=scrollBar.set)
        self.list.bind("<<ListboxSelect>>", self.onSelect)
        for item in self.info:
            self.list.insert(tk.END, item[0])
        scrollBar.config(command=self.list.yview)
        self.list.pack(side=tk.LEFT,expand=tk.YES,fill=tk.Y)
        scrollBar.pack(side=tk.LEFT,fill=tk.Y)
        leftFrame.pack(side=tk.LEFT, padx=10,pady=20, fill=tk.Y)

        #右邊的frame
        self.infoContainer = tk.Frame(self.topFrame)
        tk.Label(self.infoContainer, text=f'{self.stackname}-歷年經營績效查詢', font=('arial', 20)).pack(padx=10,pady=10)
        self.displayInfoContent(self.infoContainer, self.yearsText[0])
        #self.infoContainer.pack_propagate(0) #讓self.infoContainer的width,height有作用
        self.infoContainer.pack(side=tk.LEFT,padx=20,pady=10)

        self.topFrame.pack()

    def displayInfoContent(self,parent,year):
        if self.subFrame:
            self.subFrame.destroy() #如果已經有subFrame,則將subFrame消滅

        self.subFrame = tk.Frame(parent)
        yearindex = self.yearsText.index(year)
        valueList = self.info[yearindex]  # 儲存value內容
        titleLabelList = ['年度', '股本(億)', '財報評分', '收盤', '平均', '漲跌', '漲跌(%)', '營業收入',
                          '營業毛利', '營業利益', '業外損益', '稅後淨利', '營業毛利', '營業利益', '業外損益',
                          '稅後淨利', 'ROE(%)', 'ROA(%)', '稅後EPS', 'EPS年增(元)', 'BPS(元)']
        for labelIndex, labelText in enumerate(titleLabelList):
            rowCount = 8 #欄要顯示的數量
            rowIndex = labelIndex // rowCount
            columnIndex = labelIndex % rowCount
            tk.Label(self.subFrame, text=labelText, bg='#999999').grid(row=rowIndex * 2, column=columnIndex,
                                                                       sticky='ew')  # title的文字，分2列,0和1
            tk.Label(self.subFrame, text=valueList[labelIndex]).grid(row=(rowIndex * 2) + 1, column=columnIndex,
                                                                     sticky='ew')  # value的文字，分2列,1和3
        self.subFrame.pack()

    def buttonbox(self): #override
        '''add standard button box.
        override if you do not want the standard buttons
        '''

        boxFrame = tk.Frame(self)
        button = tk.Button(boxFrame, text="關閉", width=10, command=self.ok, default=tk.ACTIVE) #self.ok方法是繼承來的
        button.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        boxFrame.pack()

    def apply(self):
        print('apply')

    def onSelect(self,event):
        widge = event.widget
        year = widge.get(widge.curselection()[0])
        self.displayInfoContent(self.infoContainer, year)

