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


#資料查詢設定 ==========================
def Calculationstarts(self, code, startDate):
    sns.set()
    plt.style.use('fivethirtyeight')
    stockCode = self.stockIDentry.get()
    # stockCode = code
    symbol = yf.Ticker(stockCode + ".TW")
    stockName = symbol.info['symbol']                   
    stockNameC = twstock.codes[stockCode].name
    endDate = datetime.datetime.now().date()
    date_str = datetime.datetime(2021,1, 1)
    startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()


    # 下載股價資料======================================
    self.yf_df = yf.download(stockName, startDate, endDate)
    self.yf_df[['Open', 'High', 'Low', 'Close', 'Adj Close']] = self.yf_df[['Open', 'High', 'Low', 'Close', 'Adj Close']].round(2)
    self.yf_df['DailyChange%'] = round((self.yf_df['Close'].pct_change())*100,2)
    self.yf_df['5MA'] = self.yf_df['Close'].rolling(window=5).mean()
    self.yf_df['20MA'] = self.yf_df['Close'].rolling(window=20).mean()
    self.yf_df['BIAS%'] =round((self.yf_df['Close'] - self.yf_df['20MA']) / self.yf_df['20MA'] * 100,2)
    self.yf_df.dropna(inplace=True)

    for index, row in self.yf_df.iterrows():
        date = index.strftime('%Y-%m-%d')
        open_price = str(row['Open'])
        high_price = str(row['High'])
        low_price = str(row['Low'])
        close_price = str(row['Close'])
        adj_close_price = str(row['Adj Close'])
        volume = str(row['Volume'])
        daily_change = str(row['DailyChange%'])
        BIAS=str(row['BIAS%'])
        self.tree_row = (date, open_price, high_price, low_price, close_price, adj_close_price, volume, daily_change,BIAS)
        self.tree.insert("", tk.END, values=self.tree_row)
            


#《第三視窗》========================

    #個股走勢圖 ======================================

    self.fig1 = plt.figure(figsize=(8, 5))
    
    plt.title(f'{stockCode}PRICE TREND', pad=30, fontsize=20, fontweight='bold',color='#a37e67')

    
    plt.xlabel("Date",fontweight='bold',color='#749cb8', fontsize=13)
    plt.ylabel("Closing Price",fontweight='bold',color='#749cb8', fontsize=13, rotation=0, labelpad=80)
    plt.gca().xaxis.set_label_coords(0.94, -0.07)
    plt.gca().yaxis.set_label_coords(0.06, 1.02)
    plt.plot(self.yf_df["Close"], label='Close', color='navy', linewidth=1.8)
    plt.plot(self.yf_df['20MA'], label='20MA', linewidth=1.5,color='#e6880e')
    plt.legend()    

    plt.tight_layout()
    plt.xticks(fontsize=8.5, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.85)

    #self.fig1 = fig1
    self.fig1_canvas = FigureCanvasTkAgg(self.fig1, self.BigFrame3)
    self.fig1_canvas.get_tk_widget().grid(row=0, column=0, sticky="nw")


#《第四視窗》========================

    #熱力圖(數據集的特徵之間的相關性) ======================================
    self.fig2 = plt.figure(figsize=(8, 7.5))

    plt.title('熱力圖', pad=20, fontsize=20, fontweight='bold',color='#a37e67')        
    sns.set(font_scale=1.2)
    cols = ['Open', 'High', 'Low', 'Close','Adj Close','5MA','20MA','upper','lower', 'Volume']
    self.yf_df_cols = self.yf_df[cols]
    sns.heatmap(self.yf_df_cols.corr(), annot=True,annot_kws={"size": 7})
    plt.xticks(fontsize=9),plt.yticks(fontsize=9)        


    plt.tight_layout()
    #plt.subplots_adjust(left=0.05, right=1.03, bottom=0.2, top=0.85) 
    plt.subplots_adjust(left=0.07, right=1.03, bottom=0.15, top=0.9)       


    #fig2_canvas = FigureCanvasTkAgg(fig2, self.BigFrame6)
    #fig2_canvas.get_tk_widget().grid(row=0, column=0, sticky="nw")

    self.fig2_canvas = FigureCanvasTkAgg(self.fig2, self.BigFrame4) 
    self.fig2_canvas.get_tk_widget().grid(row=0, column=0, sticky="nw") 



#《第五視窗》========================
    #K線圖 ======================================
    mcolor = mpf.make_marketcolors(up='r', down='g', inherit=True)
    mstyle =mpf.make_mpf_style(base_mpf_style='yahoo',marketcolors=mcolor,rc={'font.family':'Microsoft JhengHei'})   
        
    # 繪製 K 線圖
    self.fig3,axes = mpf.plot(self.yf_df, figsize=(8, 6), returnfig=True, type='candle', mav=(5,20,60), volume=True, figratio=(8,6), figscale=1, style=mstyle, ylabel='Price', xlabel='Date', ylabel_lower='volume', xrotation=360)

    #改圖片布局(不知為何無效用)================
    self.fig3.subplots_adjust(left=0.05, right=0.98, bottom=0.05, top=0.95, wspace=0)

    self.fig3_canvas = FigureCanvasTkAgg(self.fig3,self.BigFrame5)
    #self.fig3_canvas.draw()
    self.fig3_canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)


#《第六視窗》========================
    # 盒鬚圖==============================================================
    self.fig4 = plt.figure(figsize=(8, 6.5))
    sns.boxplot(data=self.yf_df[['Open', 'High', 'Low',  'Close','5MA', '20MA']])

    plt.title('盒鬚圖', pad=20, fontsize=20, fontweight='bold',color='#a37e67')

    plt.tight_layout()
    plt.xticks(fontsize=8.5, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.subplots_adjust(left=0.15, right=0.95, bottom=0.12, top=0.85)  

    self.fig4_canvas = FigureCanvasTkAgg(self.fig4,self.BigFrame6)
    #self.fig4_canvas.draw()
    self.fig4_canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

#《第7視窗》========================
    #散點圖================================================================
    
    self.fig5=sns.pairplot(self.yf_df[['Close', 'Open', 'High', 'Low']],hue="Close",palette="husl").fig        
    plt.title('散點圖', x=1.25, y=1.9, fontsize=16)

    self.fig5_canvas = FigureCanvasTkAgg(self.fig5, self.BigFrame7)
    self.fig5_canvas.get_tk_widget().config(width=800, height=800)
    self.fig5_canvas.draw()
    self.fig5_canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)


#《第8視窗》========================


#程式撰寫=====================

    #用決策樹預測股價===================================================
    x = self.yf_df[["Open", "High", "Low", "Volume", "5MA",'20MA']]
    y = self.yf_df["Close"]
    x = x.to_numpy()
    y = y.to_numpy()
    y = y.reshape(-1, 1)
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)
    model = DecisionTreeRegressor()
    model.fit(xtrain, ytrain)
    ypred = model.predict(xtest)
    data = pd.DataFrame(data={"PredictedPrice": ypred})


    # 加入台股邏輯限制 ================================================================
    latest_close_price=self.yf_df['Close'].iloc[-1]
    data["UpperLimit"] = latest_close_price * 1.1
    data["LowerLimit"] = latest_close_price * 0.9
    data.loc[data["PredictedPrice"] > data["UpperLimit"], "PredictedPrice"] = data["UpperLimit"]
    data.loc[data["PredictedPrice"] < data["LowerLimit"], "PredictedPrice"] = data["LowerLimit"]
    tick_size = 0.01
    if latest_close_price < 10:
        tick_size = 0.01
    elif latest_close_price < 50:
        tick_size = 0.05
    elif latest_close_price < 100:
        tick_size = 0.1
    elif latest_close_price < 500:
        tick_size = 0.5
    elif latest_close_price < 1000:
        tick_size = 1
    else:
        tick_size = 5
    data["PredictedPrice_new"] = (data["PredictedPrice"] / tick_size).round() * tick_size
    data["UpperLimit_new"]=round((data["UpperLimit"][0]/tick_size).round() * tick_size,2)
    data["LowerLimit_new"]=round((data["LowerLimit"][0]/tick_size).round() * tick_size,2)
    print('最近收盤價:', latest_close_price, '次日漲停:', data["UpperLimit_new"][0], '次日跌停:', data["LowerLimit_new"][0])
    print(data.loc[:, ['PredictedPrice', 'UpperLimit_new', 'LowerLimit_new', 'PredictedPrice_new']].head(5))
    data['Difference'] = abs(data['PredictedPrice_new'] - latest_close_price)
    sorted_data = data.sort_values('Difference')
    best_prediction = round(sorted_data.iloc[1]['PredictedPrice_new'],2)
    print('最佳預測股價：', best_prediction)



# 結果呈獻=====================

    # 最佳預測股價       
    self.moneyoutputLabel.configure(text=best_prediction)
    # 股票名稱
    self.companyoutputLabel.configure(text=f'{stockCode}({stockNameC})')

