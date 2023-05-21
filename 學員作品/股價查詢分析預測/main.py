import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk
import datetime
from tkinter.simpledialog import askinteger
import calendar
from tkcalendar import Calendar 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from lxml import etree
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import twstock
import gradio as gr 
import matplotlib.font_manager as fm 
from matplotlib.font_manager import FontProperties

from backtesting import Backtest, Strategy 
from backtesting.lib import crossover 
from backtesting.test import SMA 
import pandas as pd 
from bokeh.models.formatters import DatetimeTickFormatter
import query
from download import DownloadCSV
from sma import SmaCross1, SmaCross2
from clear import clearData


#window========================

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
    #主視窗:設定===
        
        self.geometry('1400x825') 
        self.configure(background='#ffffff')  

        style1 = ttk.Style()
        #style1.configure('bg1.TFrame', background='#fcfced') 
        style1.configure('bg1.TFrame')
        style2 = ttk.Style()
        style2.configure('bg2.TFrame', background='#d5eaed')            
        mainFrame1 = ttk.Frame(self, height=825, width=450, relief=tk.RAISED, borderwidth=1, style='bg1.TFrame')
        mainFrame1.grid(row=0, column=0, sticky="nw")
        mainFrame2 = ttk.Frame(self, height=825, width=800, relief=tk.RAISED, borderwidth=1, style='bg2.TFrame')
        mainFrame2.grid(row=0, column=1, sticky="nsew")


    #八大窗格:設定

        # mainFrame1===========================
        self.BigFrame1 = tk.Frame(mainFrame1,height=100,width=450)
        self.BigFrame1.grid(row=0, column=3, rowspan=2, columnspan=2, padx=30, pady=30,sticky="nw")

        self.BigFrame2 = tk.Frame(mainFrame1,height=900,width=450)
        self.BigFrame2.grid(row=2, column=3, rowspan=2, columnspan=2, padx=5, pady=5,sticky="nw")

        ## mainFrame2 =========================
        # 用tk.Canvas()加入Scrollbar 
        canvas = tk.Canvas(mainFrame2, height=825, width=800, bg="#d5eaed")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(mainFrame2, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        
        # 將mainFrame2的所有self.BigFrame放入convas
        self.BigFrame3 = ttk.LabelFrame(canvas,height=500,width=800,text=f"趨勢圖") #趨勢圖
        canvas.create_window((0, 0), window=self.BigFrame3, anchor="nw")

        self.BigFrame4 = ttk.LabelFrame(canvas,height=750,width=800,text=f"K線圖") #K線圖
        canvas.create_window((0, 500), window=self.BigFrame4, anchor="nw")

        self.BigFrame5 = ttk.LabelFrame(canvas,height=750,width=800,text=f"熱力圖") #熱力圖
        canvas.create_window((0,1250), window=self.BigFrame5, anchor="nw")

        self.BigFrame6 = ttk.LabelFrame(canvas,height=650,width=800,text=f"盒鬚圖") #盒鬚圖
        canvas.create_window((0, 2000), window=self.BigFrame6, anchor="nw")

        self.BigFrame7 = ttk.LabelFrame(canvas,height=800,width=800,text=f"散點圖") #散點圖
        canvas.create_window((0, 2650), window=self.BigFrame7, anchor="nw")

        self.BigFrame8 = ttk.LabelFrame(canvas,height=800,width=800,text=f"績效回測") 
        canvas.create_window((0, 3450), window=self.BigFrame8, anchor="nw")

        self.BigFrame9 = ttk.LabelFrame(canvas,height=800,width=800,text=f"最終資產最佳化") 
        canvas.create_window((0, 4250), window=self.BigFrame9, anchor="nw")

        self.BigFrame10 = ttk.LabelFrame(canvas,height=800,width=800,text=f"SQN系統品質最佳化") 
        canvas.create_window((0, 5050), window=self.BigFrame10, anchor="nw")

        # # 在BigFrame3和BigFrame4之間加入一條水平線
        # canvas.create_line(0, 500, 800, 500, fill="#999999", width=1)
        
        # # 在BigFrame4和BigFrame5之間加入一條水平線
        # canvas.create_line(0, 1251, 800, 1251, fill="#999999", width=1)
        
        # # 在BigFrame5和BigFrame6之間加入一條水平線
        # canvas.create_line(0, 2002, 800, 2002, fill="#999999", width=1)

        # # 在BigFrame6和BigFrame7之間加入一條水平線
        # canvas.create_line(0, 2653, 800, 2653, fill="#999999", width=1)

        # # 在BigFrame7和BigFrame8之間加入一條水平線
        # canvas.create_line(0, 3454, 800, 3454, fill="#999999", width=1)

        # # 在BigFrame8和BigFrame9之間加入一條水平線
        # canvas.create_line(0, 4254, 800, 4254, fill="#999999", width=1)

        # # 在BigFrame9和BigFrame10之間加入一條水平線
        # canvas.create_line(0, 5054, 800, 5054, fill="#999999", width=1)

#《第一視窗：輸入》========================


    #輸入視窗================
        inputFrame = tk.Frame(self.BigFrame1)
        tk.Label(inputFrame,text="股票投資有賺有賠，\n看看就好看看就好。",font=("Arial",20,'bold'),fg="#76529c").pack()
        inputFrame.pack()
        

    #代號輸入===============
        self.stockframe = tk.Frame(self.BigFrame1,width=450)
        self.stockframe.pack()
        
        stocklabel=tk.Label(self.stockframe, text="輸入股票號碼   :",font=('Arial',15))
        stocklabel.grid(row=0,column=0,sticky=tk.W)
        
        #加上預設值，測試方便=============
        stockID_default = '2330'
        self.stockIDvar = tk.StringVar(value=stockID_default)
        
        #self.stockIDentry  = tk.Entry(self.stockframe,text=tk.StringVar(),bd=5)#不要預設值的話改回這行
        self.stockIDentry  = tk.Entry(self.stockframe,textvariable=self.stockIDvar,bd=5)
        #加上預設值，測試方便=============
        self.stockIDentry.grid(row=0, column=1, sticky=tk.W)
        code = self.stockIDentry.get() 

        
    #起始日輸入=============
        datelabel=tk.Label(self.stockframe, text="輸入查詢起始日:",font=('Arial',15))
        datelabel.grid(row=1,column=0,sticky=tk.W)

        #加上預設值，測試方便=============
        Date_default = '2022-01-01'
        self.Datevar = tk.StringVar(value=Date_default)
        
        #self.dateentry  = tk.Entry(self.stockframe,text=tk.StringVar(),bd=5)
        self.dateentry  = tk.Entry(self.stockframe,textvariable=self.Datevar,bd=5)
        #加上預設值，測試方便=============
        self.dateentry.grid(row=1, column=1,sticky=tk.W)        
        # startDate = self.dateentry.get()        
        # query.Calculationstarts(self, code, startDate) # 將 self 傳遞給 Calculationstarts 函式        
            
    #按鈕設定==============
        self.enterFrame = tk.Frame(self.BigFrame1)
        self.enterFrame.pack()

        subminButton1  = tk.Button(self.enterFrame, font=('Microsoft JhengHei',15),text="搜尋",command=query.Calculationstarts)
        subminButton1.grid(row=0, column=0, padx=(0,0))

        subminButton2  = tk.Button(self.enterFrame, font=('Microsoft JhengHei',15),text="下載歷史資料",command=DownloadCSV)
        subminButton2.grid(row=0, column=1, padx=(5,0))

        subminButton3  = tk.Button(self.enterFrame, font=('Microsoft JhengHei',15),text="績效回測",command=SmaCross1)
        subminButton3.grid(row=0, column=2, padx=(5,0))

        subminButton4  = tk.Button(self.enterFrame, font=('Microsoft JhengHei',15),text="優化策略",command=SmaCross2)
        subminButton4.grid(row=0, column=3, padx=(5,0))
        
        subminButton5  = tk.Button(self.enterFrame, font=('Microsoft JhengHei',15),text="清除",command=clearData)
        subminButton5.grid(row=0, column=4, padx=(5,0))
        


    #產出視窗==================
        self.outputFrame = tk.Frame(self.BigFrame1)
        self.outputFrame.pack(side=tk.LEFT)

    #公司名稱標籤================
        self.companynameLabel = tk.Label(self.outputFrame, text="股票名稱:", font=("Arial",15))
        self.companynameLabel.grid(row=0, column=0, sticky=tk.W, padx=10,pady=10)
        
        self.companyoutputLabel = tk.Label(self.outputFrame)
        self.companyoutputLabel.configure(text="______________", font=("Arial",15),bg="#F0F0F8")
        self.companyoutputLabel.grid(row=0, column=1, sticky=tk.W, padx=10,pady=10)       
        

    #股價預測標籤================
        self.moneynameLabel = tk.Label(self.outputFrame, text="股價預測:", font=("Arial",15))
        self.moneynameLabel.grid(row=1, column=0, sticky=tk.W, padx=10,pady=10)
        
        self.moneyoutputLabel = tk.Label(self.outputFrame)
        self.moneyoutputLabel.configure(text="______________", font=("Arial",15),bg="#F0F0F8")
        self.moneyoutputLabel.grid(row=1, column=1, sticky=tk.W, padx=10,pady=10)   


#《第二視窗》========================
        self.historyFrame = ttk.LabelFrame(self.BigFrame2,text=f"歷史股價")
        self.historyFrame.pack()

        columns = ('#1','#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9')
        self.tree = ttk.Treeview(self.historyFrame, columns=columns, show='headings')        
        self.tree.configure(height=22)
        self.tree.heading('#1', text='日期')
        self.tree.column("#1", minwidth=0, width=80)
        self.tree.heading('#2', text='開盤')
        self.tree.column("#2", minwidth=0, width=48)
        self.tree.heading('#3', text='最高')
        self.tree.column("#3", minwidth=0, width=48)
        self.tree.heading('#4', text='最低')
        self.tree.column("#4", minwidth=0, width=48)
        self.tree.heading('#5', text='收盤')
        self.tree.column("#5", minwidth=0, width=48)
        self.tree.heading('#6', text='還原收盤')
        self.tree.column("#6", minwidth=0, width=55)
        self.tree.heading('#7', text='成交量')
        self.tree.column("#7", minwidth=0, width=85)
        self.tree.heading('#8', text='漲跌幅%')
        self.tree.column("#8", minwidth=0, width=55)
        self.tree.heading('#9', text='BIAS%')
        self.tree.column("#9", minwidth=0, width=48)
        self.tree.pack(side=tk.LEFT)


        #幫treeview加scrollbar------------------------------------------------
        scrollbar = ttk.Scrollbar(self.historyFrame,command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

            





#結束===================================
def main():
    window = Window()
    window.title("台美股價格查詢預測系統")
    imge = tk.PhotoImage(file='icon2.png')
    window.iconphoto(False,imge)
    window.mainloop()

if __name__ == "__main__":
    main()
