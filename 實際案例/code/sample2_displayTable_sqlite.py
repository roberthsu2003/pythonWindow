#!usr/bin/python3.8
'''
使用tkinter label和grid顯示表格資料
顯示台積電.csv
'''
import tkinter as tk
from tkinter import *
import sqlite3


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font', ('verdana', 12, 'bold'))
        self.title("載入台積電.csv")
        self.topFrame = Frame(self,bg="#555555", width=600, height=200, padx=10, pady=10)
        self.topFrame.pack()
        bottomFrame = Frame(self)
        Button(bottomFrame, text='載入sqlite', command=self.buttonClick).pack()
        bottomFrame.pack(padx=10, pady=10)

    def buttonClick(self):
        displayData=readSQLite()
        for rowindex,row in enumerate(displayData):
            for cellIndex,cellItem in enumerate(row):
                cellFrame = Frame(self.topFrame,bg='#555555')
                Label(cellFrame,text=cellItem,bg='#555555',fg='#FFFFFF').pack()
                cellFrame.grid(row=rowindex,column=cellIndex)

def toString(value):
    if not isinstance(value,str):
        if value is None:
            return "-"
        else:
            return str(value)
    return value

def readSQLite():
    datalist = [];
    datalist.append(['年度','股本(億)','財報評分','收盤','平均','漲跌','漲跌(%)','營業收入',
                     '營業毛利','營業利益','業外損益','稅後淨利','營業毛利','營業利益','業外損益',
                     '稅後淨利','ROE(%)','ROA(%)','稅後EPS','EPS年增(元)','BPS(元)'])
    conn = sqlite3.connect('台積電.db')
    print("開啟資料庫成功")
    c = conn.cursor()
    cursor = c.execute("select * from 獲利指標")
    for row in cursor:
        rowList = []
        for cell in row:
           rowList.append(toString(cell))
        datalist.append(rowList)

    print("select 成功")
    return datalist


if __name__ == "__main__":
    window = Window()
    window.mainloop()


