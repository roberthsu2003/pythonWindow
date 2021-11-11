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
            btn = tk.Button(buttonsFrame,text=year)
            btn.grid(row=rIndex,column=cIndex)
            btn.bind("<Button-1>",self.buttonClick)
        buttonsFrame.pack_propagate(0)
        buttonsFrame.pack(padx=20,pady=20)

    def buttonClick(self,event):
        pressedBtn = event.widget #取得被按按鈕的參考
        print(pressedBtn['text']) #透過參考取得按鈕的文字

