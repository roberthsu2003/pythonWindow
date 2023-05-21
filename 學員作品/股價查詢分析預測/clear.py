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



# 清除資料 ========================================================
def clearData(self):
    self.moneyoutputLabel.configure(text="______________")
    self.companyoutputLabel.configure(text="______________")
    self.stockIDentry.delete(0, tk.END)
    self.dateentry.delete(0, tk.END)
    if hasattr(self, 'fig1_canvas'):
        self.fig1.clf()
        self.fig1_canvas.draw()
        self.fig1_canvas.get_tk_widget().pack_forget()
    if hasattr(self, 'fig2_canvas'): 
        self.fig2.clf() 
        self.fig2_canvas.draw() 
        self.fig2_canvas.get_tk_widget().pack_forget()                    
    if hasattr(self, 'fig3_canvas'):
        # self.fig3.clf()
        self.fig3_canvas.draw() 
        self.fig3_canvas.get_tk_widget().pack_forget()   
    if hasattr(self, 'fig4_canvas'):
        # self.fig4.clf() 
        self.fig4_canvas.draw() 
        self.fig4_canvas.get_tk_widget().pack_forget()
    if hasattr(self, 'fig5_canvas'):
        # self.fig5.clf() 
        self.fig5_canvas.draw() 
        self.fig5_canvas.get_tk_widget().pack_forget()
    for row_id in self.tree.get_children():
        self.tree.delete(row_id)                 
    if hasattr(self, 'text1'):
        self.text1.delete("1.0", "end")
        self.text1.destroy() 
    if hasattr(self, 'result'):
        del self.result
    if hasattr(self, 'text2'):
        self.text2.delete("1.0", "end")
        self.text2.destroy() 
    if hasattr(self, 'text3'):
        self.text3.delete("1.0", "end")
        self.text3.destroy() 