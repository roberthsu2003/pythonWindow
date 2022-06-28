import tkinter.ttk as ttk
import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from datetime import datetime

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("台積電當日線圖")
        mainFrame  = tk.Frame(self, relief="groove", borderwidth=2)
        titleFrame = tk.Frame(mainFrame)
        tk.Label(titleFrame,text="台積電當日線圖",font=("Arial",20,'bold'),fg="#555555").pack(padx=10)
        titleFrame.pack(pady=30)
        self.datetimeLabel = tk.Label(titleFrame, text="", font=("Arial", 20), fg="#555555")
        self.datetimeLabel.pack(padx=10)
        titleFrame.pack(pady=30)

        columns = ('#1', '#2', '#3', '#4', '#5')
        self.tree = ttk.Treeview(mainFrame, columns=columns, show='headings')

        # define headings
        self.tree.heading('#1', text='公司名')
        self.tree.heading('#2', text='交易時間')
        self.tree.heading('#3', text="成交價")
        self.tree.heading('#4', text="漲跌價")
        self.tree.heading('#5', text="百分比")
        self.tree.pack()

        mainFrame.pack(pady=30,padx=30,ipadx=30,ipady=30)
        #-----------建立顯示畫面-----------------------
        self.panel = tk.Label(self)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.repeatRun()

    def repeatRun(self):
        #顯示時間
        now = datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S")
        self.datetimeLabel.configure(text=now_string)

        #載入csv
        file_name = now.strftime("./assets/%Y-%m-%d.csv")
        dataFrame = pd.read_csv(file_name)
        dataFrame.columns = ["公司名","日期","成交價","漲跌價","百分比"]
        unique_dataFrame = dataFrame.drop_duplicates()

        #清除treeview data
        for i in self.tree.get_children():
            self.tree.delete(i)

        #加入treeview的內容
        unique_lists= list(unique_dataFrame.values)
        unique_lists.reverse()
        for items in unique_lists:
            self.tree.insert('', tk.END, values=list(items))



        self.after(1000,self.repeatRun)

def closeWindow():
    print("close window")
    window.destroy()



if __name__ == "__main__":
    window = Window()
    window.resizable(width=0,height=0)
    window.protocol("WM_DELETE_WINDOW",closeWindow)
    window.mainloop()




