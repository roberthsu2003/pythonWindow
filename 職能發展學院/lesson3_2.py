#!usr/bin/python3.8
"""
這是我的python_window範例
"""
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import requests

urlpath = '	https://data.epa.gov.tw/api/v1/aqx_p_02?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&sort=ImportDate%20desc&format=json'

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = ttk.LabelFrame(self,text="上方選項")
        labelFont = tkFont.Font(family="Arial", size=30)
        label = ttk.Label(topFrame,text='Hello World',font=labelFont,anchor=tk.CENTER)
        label.pack(padx=20,pady=10)
        leftbutton = ttk.Button(topFrame,text="確定",command=self.topLeftClick)
        leftbutton.pack(side=tk.LEFT,pady=10,ipady=10,padx=20)
        rightbutton = ttk.Button(topFrame, text="取消",command=self.topRightClick)
        rightbutton.pack(side=tk.RIGHT, pady=10, ipady=10,padx=20)
        topFrame.pack(padx=10,pady=10)

        buttonFrame = ttk.LabelFrame(self, text="下方顯示")
        tree = ttk.Treeview(buttonFrame, columns=['1', '2', '3'], show='headings')
        tree.column('1', width=100, anchor='center')
        tree.column('2', width=100, anchor='center')
        tree.column('3', width=100, anchor='center')
        tree.heading('1', text='姓名')
        tree.heading('2', text='學號')
        tree.heading('3', text='性別')
        tree.insert('', 'end', values='l1')
        tree.insert('', 'end', values='l2')
        tree.insert('', 'end', values='l3')
        tree.pack()
        buttonFrame.pack(padx=10, pady=10)

    def topLeftClick(self):
        response = requests.get(urlpath)
        if response.status_code == 200:
            dataList = response.json()['records']
        print(dataList)


    def topRightClick(self):
        print("right click")



if __name__ == "__main__":
    window = Window()
    window.title('class的寫法')
    #window.geometry('300x300')
    #window.config(bg='blue')
    window.mainloop()