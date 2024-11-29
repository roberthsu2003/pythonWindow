import pandas as pd
import numpy as np
import requests
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import outsources
import datasource
import mplfinance
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import sqlite3

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Stock Analysis")
        self.geometry('1800x600')
        
        #==========STYLE===========
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        style.configure('All.TButton',font=('Helvetica',14))
        #==========END style============
        
        #===========RightFrame=============
        self.rightFrame= ttk.Frame(self,borderwidth=2,relief='groove',width=1050, height=600)

        #===========canvas area=============
        self.canvas_area = tk.Canvas(self.rightFrame,width=1050, height=600, bg="white")
        
        self.current = self.add_image(self.rightFrame,'stock.jpg')
    
        self.canvas_area.pack()
         #===========end canvas area=============
        self.rightFrame.pack(side='right',padx=10,pady=10)
        #=========RightFrame END===========

        
        #===========leftFrame=============
        self.leftFrame = ttk.Frame(self)

                #==TOPFRAME=====
        self.topFrame = ttk.Frame(self.leftFrame)
        ttk.Label(self.topFrame,text='台積電股票預測',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(pady=10)
        self.icon_button = outsources.ImageButton(self.topFrame,command=self.update_treeview)
        self.icon_button.pack(pady=7,side='right',padx=5)
        ttk.Label(self.topFrame,text=' 起始數據: 2020-01-01',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(ipadx=5,pady=10)
        self.topFrame.pack(fill='x')
                #==TOPFRAME END=====
           #=== 分析方法===
        self.analysisFrame = ttk.Frame(self.leftFrame)
        self.linear_btn = ttk.Button(self.analysisFrame,text='線性回歸分析',style='All.TButton',command=self.plot_regression)
        self.linear_btn.grid(row=0,column=0,padx=5,pady=5)
        self.linear_btn = ttk.Button(self.analysisFrame,text='RSI',style='All.TButton',command=self.plot_rsi)
        self.linear_btn.grid(row=0,column=1,padx=5,pady=5)
        self.linear_btn = ttk.Button(self.analysisFrame,text='MACD',style='All.TButton',command=self.plot_macd)
        self.linear_btn.grid(row=1,column=0,padx=5,pady=5)
        self.linear_btn = ttk.Button(self.analysisFrame,text='MA',style='All.TButton',command=self.plot_sma)
        self.linear_btn.grid(row=1,column=1,padx=5,pady=5)

        self.analysisFrame.pack(fill='x',pady=10)

           #=== 分析方法end===
            #===預測分析=====
        self.resultFrame = ttk.Frame(self.leftFrame)
        ttk.Label(self.resultFrame,text='預測分析',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid()
        ttk.Label(self.resultFrame,text='明日股價',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid(row=0,column=0,padx=5,pady=5)
        self.result_entry = ttk.Entry(self.resultFrame)
        self.result_entry.grid(row=0,column=1,padx=15,pady=5)
        self.resultFrame.pack(fill='x', pady=10)
                #=== 預測分析 end===
        
            #=== 資料庫 frame===
        self.databaseFrame = ttk.Frame(self.leftFrame)
        self.tree_scrollbar = ttk.Scrollbar(self.databaseFrame, orient="vertical")
            #=== tree viw frame===

        self.tree = ttk.Treeview(self.databaseFrame,columns=('Date', "Open", 'High', 'Low', 'Volume', "Close"),show='headings',yscrollcommand=self.tree_scrollbar.set)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Open", text="Open")
        self.tree.heading("High", text="High")
        self.tree.heading("Low", text="Low")
        self.tree.heading("Volume", text="Volume")
        self.tree.heading("Close", text="Close")

        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Open", width=50, anchor="center")
        self.tree.column("High", width=50, anchor="center")
        self.tree.column("Low", width=50, anchor="center")
        self.tree.column("Volume", width=100, anchor="center")
        self.tree.column("Close", width=50, anchor="center")

        

        # 使用 grid 布局確保滾動條在右側
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_scrollbar.grid(row=0, column=1, sticky="ns")  # 垂直填滿右側
        
        self.tree_scrollbar.config(command=self.tree.yview)
             #=== tree viw frame end===
        # 配置滾動條與 Treeview 的交互
        self.databaseFrame.pack(padx=10)
        
            #=== 資料庫 frame end===
        self.load_data()

        self.leftFrame.pack(side='left',fill='y',padx=10,pady=10)


        #=========leftFrame END===========



    def add_image(self,frame,image_path):
        
        img = Image.open('stock.jpg')
        resized_img = img.resize((1050, 600), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_img)

        img_label = tk.Label(frame,image=photo)
        img_label.image = photo
        img_label.pack()
        
    
    def plot_regression(self):
        fig = datasource.linear_regression()
        model,data_from_db = datasource.get_model_and_data()
        firstdat_predict = datasource.get_future_day1_price(model,data_from_db)
        self.result_entry.delete(0,tk.END)
        self.result_entry.insert(0,f'{firstdat_predict:.2f}')

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)

    def plot_rsi(self):
        self.result_entry.delete(0,tk.END)
        fig = datasource.rsi()

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)
    
    def plot_sma(self):
        self.result_entry.delete(0,tk.END)
        fig = datasource.sma()

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)

    def plot_macd(self):
        self.result_entry.delete(0,tk.END)
        fig = datasource.macd()

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)

    def load_data(self):
         # 連接到 SQLite 資料庫
        conn = sqlite3.connect('check_data.db')

        # 從資料庫讀取資料
        sql = sql = '''SELECT Date, Open, High, Low, Volume, Close FROM NewTable'''
        data_from_db = pd.read_sql(sql, conn)

        # 關閉資料庫連接
        conn.close()

        for _,row in data_from_db.iterrows():
            self.tree.insert("","end",values=row.tolist())
    
    def update_treeview(self):
        datasource.download_data()
        # Step 2: 清除 Treeview 的現有資料
        self.tree.delete(*self.tree.get_children())

        # Step 3: 重新加載最新資料到 Treeview
        self.load_data()




    

def main():
    def on_closing():
        print("Exiting...")
        window.destroy()
        sys.exit()
    window= Window(theme='clam')
    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()
    


if __name__ == '__main__':
    main()

