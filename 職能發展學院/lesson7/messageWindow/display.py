import tkinter as tk

class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        self.yearsText = [secondList[0] for secondList in dataList]
        tk.Label(self,text=f'{stockName}歷年經營績效查詢',font=('arial',20)).pack(padx=10,pady=10)
        #建立buttonsFrame
        buttonsFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300,height=80)
        for yearIndex,year in enumerate(self.yearsText):
            print(f'{yearIndex},{year}')
        buttonsFrame.pack_propagate(0)
        buttonsFrame.pack(padx=20,pady=20)

