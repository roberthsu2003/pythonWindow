import tkinter as tk

class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        tk.Label(self,text=f'{stockName}歷年經營績效查詢',font=('arial',20)).pack(padx=10,pady=10)
        #建立buttonsFrame
        buttonsFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300,height=80)
        tk.Button(buttonsFrame,text="2021").pack()
        buttonsFrame.pack_propagate(0)
        buttonsFrame.pack(padx=20,pady=20)

