import tkinter as tk

class Display(tk.Toplevel):
    def __init__(self, main,stockName,dataList):
        super().__init__(main)
        print(stockName)
        for item in dataList:
            print(item)
