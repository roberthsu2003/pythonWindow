#!usr/bin/python3.8
'''
使用tkinter label和grid顯示表格資料
顯示台積電.csv
'''
import tkinter as tk
from tkinter import *
import csv


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font', ('verdana', 12, 'bold'))
        self.title("載入台積電.csv")
        self.topFrame = Frame(self,bg="#555555", width=600, height=200, padx=10, pady=10)
        self.topFrame.pack()
        bottomFrame = Frame(self)
        Button(bottomFrame, text='載入CSV檔', command=self.buttonClick).pack()
        bottomFrame.pack(padx=10, pady=10)

    def buttonClick(self):
        displayData=readCSV("台積電.csv")
        for rowindex,row in enumerate(displayData):
            for cellIndex,cellItem in enumerate(row):
                cellFrame = Frame(self.topFrame,bg='#555555')
                Label(cellFrame,text=cellItem,bg='#555555',fg='#FFFFFF').pack()
                cellFrame.grid(row=rowindex,column=cellIndex)


def readCSV(fileName):
    datalist = [];
    try:
        file=open("台積電.csv","r",encoding='utf8')
    except EXCEPTION as e:
        print("讀取錯誤發生錯誤",e)
        return None

    rows = csv.reader(file)
    for row in rows:
        datalist.append(row)
    return datalist


if __name__ == "__main__":
    window = Window()
    window.mainloop()


