import tkinter as tk
from .gethistorydata import get_history_data,read_history_data
from datetime import datetime,timedelta
from chinese_calendar import is_workday

class line_opt_frame(tk.Toplevel):
    def __init__(self,main,stockName):
        super().__init__(main)

        self.title(f"LINE通知設定")

        '''自動抓視窗位置'''
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        self.geometry(f'+{width // 2 - 600}+{height // 2 - 300}')
        '''自動抓視窗位置'''

