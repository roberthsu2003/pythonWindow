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



# 產出 CSV 檔案 ========================================================
def DownloadCSV(self):
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
    if file_path:
        #stockCode = self.stockIDentry.get()
        #self.Calculationstarts()
        #self.yf_df.to_csv(file_path + f'./{stockCode}_tw_stock.csv', index=False)
        self.yf_df.to_csv(file_path)


