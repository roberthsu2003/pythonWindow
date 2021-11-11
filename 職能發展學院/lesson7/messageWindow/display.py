import tkinter as tk

class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        tk.Label(self,text=f'{stockName}歷年經營績效查詢').pack(padx=10,pady=10)

