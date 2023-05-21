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



def SmaCross1(self):
    if hasattr(self, 'text1'):
        self.text1.destroy() 
    class SmaCross(Strategy):
        n1=5
        n2=20
        def init(self):
            self.sma1 = self.I(SMA, self.data.Close, self.n1) 
            self.sma2 = self.I(SMA, self.data.Close, self.n2) 
            
        def next(self):
            if crossover(self.sma1, self.sma2): 
                self.buy()
            elif crossover(self.sma2, self.sma1): 
                self.sell()

    self.test = Backtest(self.yf_df, SmaCross, cash=1000000, commission=.004,exclusive_orders=True,trade_on_close=True)
    self.result = self.test.run()
        
    self.text1 = tk.Text(self.BigFrame8, font=("Courier", 13), width=100, height=50)
    self.text1.pack(expand=True, fill="both")
    self.text1.insert("end", self.result.to_string(index=True))


#《第9視窗》========================
def SmaCross2(self):
    if hasattr(self, 'text2'):
        self.text2.destroy()   
    if hasattr(self, 'text3'):
        self.text3.destroy()   
    self.opt_result_equity = self.test.optimize(n1=range(5, 50, 5),n2=range(10, 120, 5),maximize='Equity Final [$]',constraint=lambda p: p.n1 < p.n2)  

    self.text2 = tk.Text(self.BigFrame9, font=("Courier", 13), width=100, height=50)
    self.text2.pack(expand=True, fill="both")
    self.text2.insert("end", self.opt_result_equity.to_string(index=True))

#《第10視窗》========================
    self.opt_result_sqn = self.test.optimize(n1=range(5, 50, 5),n2=range(10, 120, 5),maximize='SQN',constraint=lambda p: p.n1 < p.n2)  

    self.text3 = tk.Text(self.BigFrame10, font=("Courier", 13), width=100, height=50)
    self.text3.pack(expand=True, fill="both")
    self.text3.insert("end", self.opt_result_sqn.to_string(index=True))


