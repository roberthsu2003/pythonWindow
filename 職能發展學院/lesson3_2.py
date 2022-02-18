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
        tree = ttk.Treeview(buttonFrame, columns=['site', 'county', 'pm25','date','unit'], show='headings')
        tree.column('site', width=100, anchor='center')
        tree.column('county', width=100, anchor='center')
        tree.column('pm25', width=100, anchor='center')
        tree.column('date', width=100, anchor='center')
        tree.column('unit', width=100, anchor='center')
        tree.heading('site', text='站點')
        tree.heading('county', text='城市')
        tree.heading('pm25', text='PM2.5')
        tree.heading('date', text='日期')
        tree.heading('unit', text='單位')
        tree.insert('', 'end', values=['l1','l2','l3'])
        tree.insert('', 'end', values=('o1','o2','o3'))
        tree.insert('', 'end', values=('j1','j2','j3'))
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