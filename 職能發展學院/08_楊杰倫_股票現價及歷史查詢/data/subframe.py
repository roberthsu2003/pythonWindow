import tkinter as tk
from .gethistorydata import get_history_data,read_history_data
from .user_option import load_history_option,save_history_option
from datetime import datetime,timedelta
from chinese_calendar import is_workday
from tkinter import ttk

class subframe(tk.Toplevel):
    def __init__(self,main,stockName):
        super().__init__(main)

        self.title(f"{stockName}歷史資料查詢")
        '''自動抓視窗位置'''
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        self.geometry(f'+{width // 2 - 600}+{height // 2 - 300}')
        '''自動抓視窗位置'''
        self.stockName = stockName
        self.timedelta = tk.IntVar()
        self.page_display_num=tk.IntVar()

        try:
            history_option = load_history_option()
            self.timedelta.set(int(history_option[0]))
            self.page_display_num.set(str(history_option[1]))
        except:
            self.timedelta.set("7")
            self.page_display_num.set("20")


        frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)
        frame3 = tk.Frame(self)
        self.frame4 = tk.Frame(self)


        tk.Label(frame1, text=f"{self.stockName} 歷史資料查詢",padx=10, pady=10,font=(15)).pack(side=tk.TOP)
        self.status_label = tk.Label(self.frame2, text=f"", padx=10, pady=10,fg="green")
        self.status_label.pack(side=tk.LEFT)
        tk.Button(frame3, text='下載資料', padx=10, pady=1, command=self.download).pack(side=tk.LEFT)
        tk.Button(frame3, text='顯示資料', padx=10, pady=1, command=self.display_history_data).pack(side=tk.LEFT)
        tk.Button(frame3, text='設定區間', padx=10, pady=1, command=self.display_history_data).pack(side=tk.LEFT)
        tk.Label(frame3, text="", padx=10, pady=10,fg="green").pack(side=tk.LEFT)   #這個label不顯示東西，排版用的
        tk.Entry(frame3, textvariable=self.timedelta, width=10).pack(side=tk.LEFT)

        tk.Label(frame3, text="每頁顯示的筆數", padx=10, pady=10, fg="green").pack(side=tk.LEFT)
        tk.Entry(frame3, textvariable=self.page_display_num, width=10).pack(side=tk.LEFT)


        frame1.pack(side=tk.TOP, fill=tk.X)
        self.frame2.pack(side=tk.TOP, fill=tk.X)
        frame3.pack(side=tk.TOP, fill=tk.X)
        self.frame4.pack(side=tk.TOP, fill=tk.X)

        self.display_history_data()



    def download(self):
        '''下載功能，之後呼叫顯示列表標題'''

        save_history_option(self.timedelta.get(),self.page_display_num.get())

        false_code = False
        #嘗試下載
        self.history_data = get_history_data(self.stockName[:4])
        if self.history_data == None:
            false_code = True
        else:
            self.status_label.config(text="下載完成", fg="green")
        self.display_history_data(false_code)

    def display_history_data(self,false_code=False):
        '''顯示列表標題，顯示title和計算工作日並提供時間給顯示內容'''

        save_history_option(self.timedelta.get(),self.page_display_num.get())
        '''嘗試讀取資料'''
        try:
            all_history_data = read_history_data()[self.stockName[:4]]
            tk.Label(self.frame2, text=f"", padx=10, pady=10, fg="green").pack(side=tk.LEFT)
        except:
            if false_code:
                self.status_label.config(text="查無資料",fg="red")
            else:
                self.status_label.config(text="尚未下載過此資料", fg="red")
        '''嘗試讀取資料'''



        '''嘗試清空，不然第2次顯示時容易有bug'''
        try:
            for item in self.grid_list:
                item.grid_forget()
            for item in self.grid_title:
                item.grid_forget()
        except:
            pass
        '''嘗試清空，不然第2次顯示時容易有bug'''

        self.grid_title = []
        self.grid_list = []
        self.grid_list_count  = 0
        self.row = 0

        days_timedelta = 0
        work_day = 0
        set_display_day = self.timedelta.get()

        '''運算出工作日，並呼叫顯示內容'''
        while work_day < set_display_day:
            if is_workday((datetime.now() - timedelta(days= days_timedelta)).date()):
                year = int((datetime.now() - timedelta(days=days_timedelta)).strftime('%Y'))
                month = int((datetime.now() - timedelta(days=days_timedelta)).strftime('%m'))
                day = int((datetime.now() - timedelta(days=days_timedelta)).strftime('%d'))

                serch_time = str(int(datetime(year, month, day, 8).timestamp()) * 1000)
                if self.display_history_content(all_history_data, serch_time):
                    work_day += 1
            days_timedelta+=1
        '''運算出工作日，並呼叫顯示內容'''

    def display_history_content(self,all_history_data,serch_time):
        '''顯示內容功能'''

        '''取得每頁要顯示的筆數+計算位移)'''
        page_num_option = int(self.page_display_num.get())
        next_page = len(self.grid_list)//(page_num_option * 10)
        row_delta = (next_page * page_num_option-1)
        '''取得每頁要顯示的筆數+計算位移)'''

        '''顯示標題+計算位移)'''
        if len(self.grid_list)%(page_num_option * 10 - page_num_option) == page_num_option*next_page:
            key_list = ['日期', '收盤價', '外資持股率', '外資', '投信', '自營商', '三大法人', '開盤價', '最高價', '最低價']
            # ['外資', '投信', '自營商', '三大法人', '外資持股率', '股價']
            for title_key in range(len(key_list)):
                self.grid_title.append(tk.Label(self.frame4, text=f"{key_list[title_key]}", padx=10, pady=10))
                self.grid_title[-1].grid(row=0,column=title_key+next_page*10)
        '''顯示標題+計算位移)'''

        #資料的key
        key_list=['股價', '外資持股率','外資', '投信', '自營商', '三大法人', '股價','股價','股價']

        '''顯示資料日期+計算位移'''
        a = datetime.fromtimestamp(int(serch_time) / 1000)  # /1000回來，原因請看serch_time來源
        week = self.trans_week(a)
        self.grid_list.append(
            tk.Label(self.frame4, text=f"{datetime.strptime(str(a), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d' + week)}",padx=10, pady=10))
        self.grid_list[-1].grid(row=1 + self.row - row_delta, column=0 + next_page * 10)
        '''顯示資料日期+計算位移'''

        count_fail = 0
        '''最後以下顯示其他資料+計算位移'''
        for column in range(0,len(key_list)):
            try:
                '''透過日期定位嘗試取得資料內容，若無則顯示"-"'''
                index = all_history_data[key_list[column]].index(serch_time)
                if column == 0:
                    text = all_history_data[key_list[column]][index + 4]
                    self.grid_list.append(tk.Label(self.frame4, text=text, padx=10,pady=10))
                    self.grid_list[-1].grid(row=1 + self.row-row_delta, column=column + 1+next_page*10)
                elif column == 1:   #因為外資持股率資料來源還沒出來的話，他會給0而不會拋出錯誤，因此修正此數值
                    text = all_history_data[key_list[column]][index + 1]+"%"
                    if text == "0%":
                        text = "尚無資料"
                    self.grid_list.append(tk.Label(self.frame4, text=text, padx=10,pady=10))
                    self.grid_list[-1].grid(row=1 + self.row-row_delta, column=column + 1+next_page*10)
                elif column == 5:
                    text = all_history_data[key_list[column]][index + 1]
                    if int(text) >0:
                        self.grid_list.append(tk.Label(self.frame4, text=text, padx=10,pady=10,fg="red"))
                    elif int(text)<0:
                        self.grid_list.append(tk.Label(self.frame4, text=text, padx=10, pady=10,fg="green"))
                    self.grid_list[-1].grid(row=1 + self.row-row_delta, column=column + 1+next_page*10)
                elif column == 7:
                    text = all_history_data[key_list[column]][index + 2]
                    self.grid_list.append(tk.Label(self.frame4, text=text, padx=10,pady=10))
                    self.grid_list[-1].grid(row=1 + self.row-row_delta, column=column + 1+next_page*10)
                elif column == 8:
                    text = all_history_data[key_list[column]][index + 3]
                    self.grid_list.append(tk.Label(self.frame4, text=text, padx=10,pady=10))
                    self.grid_list[-1].grid(row=1 + self.row-row_delta, column=column + 1+next_page*10)
                else:
                    text = all_history_data[key_list[column]][index + 1]
                    self.grid_list.append(tk.Label(self.frame4, text=text, padx=10, pady=10))
                    self.grid_list[-1].grid(row=1 + self.row-row_delta, column=column + 1+next_page*10)
            except:
                self.grid_list.append(tk.Label(self.frame4, text="-", padx=10, pady=10))
                self.grid_list[-1].grid(row=1 + self.row - row_delta,column=column + 1 + next_page * 10)
                count_fail +=1


        self.grid_list_len = len(self.grid_list)
        if count_fail == 9:

            for i in range(1,11):
                self.grid_list[-1].grid_forget()
            del self.grid_list[-10:]

            self.grid_list_count+=1

            return False

        self.row += 1
        return True



    def trans_week(self,a):
        '''轉換星期'''
        english_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        chinese_week = ["(一)","(二)","(三)","(四)","(五)","(六)","(日)"]
        for i in range(7):
            if datetime.strptime(str(a), '%Y-%m-%d %H:%M:%S').strftime('%A') == english_week[i]:
                return chinese_week[i]