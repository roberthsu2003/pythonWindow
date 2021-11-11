import tkinter as tk

class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        self.yearsText = [secondList[0] for secondList in dataList]
        print(self.yearsText)
        tk.Label(self,text=f'{stockName}歷年經營績效查詢',font=('arial',20)).pack(padx=10,pady=10)
        #建立buttonsFrame
        buttonsFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300,height=80)
        for rowIndex in range(4):
            for columnIndex in range(6):
                tk.Button(buttonsFrame,text=f"row={rowIndex},column={columnIndex}").grid(row=rowIndex,column=columnIndex)
        buttonsFrame.pack_propagate(0)
        buttonsFrame.pack(padx=20,pady=20)

