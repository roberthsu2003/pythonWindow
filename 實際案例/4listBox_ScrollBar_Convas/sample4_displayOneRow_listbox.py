#!usr/bin/python3.8
'''
使用tkinter listbox和顯示單筆表格資料
顯示台積電.sqlite
'''


import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font', ('verdana', 12, 'bold'))
        #self.geometry("450x400")
        self.resizable(0,0) #不允許更改視窗大小
        self.title("載入台積電sqlite,單筆資料")
        leftFrame = Frame(self)
        scrollBar = Scrollbar(leftFrame)
        self.list = Listbox(leftFrame, width=10, height=3, yscrollcommand=scrollBar.set)
        self.list.bind("<<ListboxSelect>>", self.onSelect)
        scrollBar.config(command=self.list.yview)
        self.list.pack(side=LEFT, expand=YES, fill="y")
        scrollBar.pack(side=LEFT,fill="y")
        for title in getYears():
            self.list.insert(END, title)
        leftFrame.pack(side=LEFT,padx=10, pady=10,fill="y")

        frameConvas = Canvas(self)
        convasScollbar = Scrollbar(self, orient="vertical", command=frameConvas.yview)
        self.rightFrame = Frame(frameConvas,width=200, pady=10)
        self.rightFrame.bind(
            "<Configure>",
            lambda e: frameConvas.configure(
                scrollregion=frameConvas.bbox("all")
            )
        )
        frameConvas.create_window((0, 0), window=self.rightFrame, anchor="nw")
        #self.rightFrame.pack_propagate(0) #不允許由它決定高度和寬度
        titles = ['年度','股本(億)','財報評分','收盤','平均','漲跌','漲跌(%)','營業收入',
                     '營業毛利','營業利益','業外損益','稅後淨利','營業毛利','營業利益','業外損益',
                     '稅後淨利','ROE(%)','ROA(%)','稅後EPS','EPS年增(元)','BPS(元)']
        self.values = []
        for _ in range(21):
            stringVar = StringVar()
            stringVar.set("Value")
            self.values.append(stringVar)


        for index,item in enumerate(titles):
            Label(self.rightFrame, text=item).grid(row=index, column=0,sticky=W, padx=10, pady=5)
        for index,item in enumerate(self.values):
            Label(self.rightFrame, textvariable= item ).grid(row=index, column=1)
        #self.rightFrame.pack(side=LEFT,expand=YES,fill="x")

        frameConvas.config(yscrollcommand=convasScollbar.set)
        frameConvas.pack(side=LEFT,expand=YES,fill=BOTH)
        convasScollbar.pack(side=RIGHT,fill="y")

    def onSelect(self,event):
        widge = event.widget
        value = widge.get(widge.curselection()[0])
        record=getOneRecord(value)
        for index,value in enumerate(self.values):
            value.set(record[index])



def toString(value):
    if not isinstance(value,str):
        if value is None:
            return "-"
        else:
            return str(value)
    return value


def getYears():
    years = []
    conn = sqlite3.connect('台積電.db')
    print("開啟資料庫成功")
    c = conn.cursor()
    cursor =c.execute("select 年度 from 獲利指標")
    for row in cursor:
        years.append(row[0])
    print("select 成功")
    conn.close()
    return years

def getOneRecord(year):
    record = []
    conn = sqlite3.connect('台積電.db')
    c = conn.cursor()
    cursor = c.execute("select * from 獲利指標 where 年度= ?",[year])
    print(cursor)
    for columns in cursor:
        #cursor內只有一筆，抓出來是tuple
        for column in columns:
            record.append(toString(column))
    conn.close()
    return record



if __name__ == "__main__":
    window = Window()
    window.list.select_set(0)
    window.list.event_generate("<<ListboxSelect>>")
    window.mainloop()


