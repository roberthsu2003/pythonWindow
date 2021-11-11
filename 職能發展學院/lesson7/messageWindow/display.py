import tkinter as tk

columnCount = 8
class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        self.yearsText = [secondList[0] for secondList in dataList]
        tk.Label(self,text=f'{stockName}歷年經營績效查詢',font=('arial',20)).pack(padx=10,pady=10)
        #建立buttonsFrame
        buttonsFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300,height=80)
        for yearIndex,year in enumerate(self.yearsText):
            rIndex = yearIndex // columnCount  #求得按鈕row的索引編號
            cIndex = yearIndex % columnCount #求得按鈕column的索引編號
            tk.Button(buttonsFrame,text=year).grid(row=rIndex,column=cIndex)

        buttonsFrame.pack_propagate(0)
        buttonsFrame.pack(padx=20,pady=20)

