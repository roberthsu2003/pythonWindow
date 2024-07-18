#自定義 套件
import data_loading as rdata
import datas
from datas import Data
import features
from features.feature import Feature
#python 套件
import tkinter 
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from numpy import random    #亂數產生
import numpy as np       #數學處理
import matplotlib.pyplot as plt #繪圖
import seaborn as sns
from sklearn.feature_selection import SelectKBest,f_regression
from sklearn.feature_selection import chi2

class Window(ThemedTk):
    def __init__(self,**kwargs):
        self._stock_id:int=0
        self._stock_data:pd.DataFrame=None
        self._stock_features:list=[]

        super().__init__(**kwargs)
        self.title("stock window")
        self.geometry("800x600")

        style = ttk.Style()
        style.configure("LeftTop.TFrame", background="lightblue")
        style.configure("LeftBottom.TFrame", background="lightgreen")
        style.configure("Right.TFrame", background="lightcoral")

        main_frame=ttk.Frame(self)
        #main_frame的設定 
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        #左-------------------------------------------------------------------------------------------
        self.left_frame=ttk.Frame(main_frame)
        #left_frame的設定
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.left_top_frame = ttk.Frame(self.left_frame, style="LeftTop.TFrame")

        self.stock_id_var = tkinter.StringVar()

        self.choose_date()

        self.left_top_frame.grid(row=0, column=0, sticky="nsew")

        self.left_bottom_frame = ttk.Frame(self.left_frame, style="LeftBottom.TFrame")

        self.left_bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.left_frame.grid(row=0,column=0,sticky="nsew")
        #左-------------------------------------------------------------------------------------------

        #右-------------------------------------------------------------------------------------------
        self.right_frame = ttk.Frame(main_frame, style="Right.TFrame")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        canvas = tkinter.Canvas(self.right_frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbarx = ttk.Scrollbar(self.right_frame, orient="horizontal", command=canvas.xview)
        scrollbary = ttk.Scrollbar(self.right_frame, orient="vertical", command=canvas.yview)
        scrollbarx.grid(row=1, column=0, sticky="ew")
        scrollbary.grid(row=0, column=1, sticky="ns")
        canvas.configure(xscrollcommand=scrollbarx.set,yscrollcommand=scrollbary.set)

        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        #右-------------------------------------------------------------------------------------------
        main_frame.pack(fill="both", expand=True)
    
    @property
    def stock_id(self):
        return self._stock_id
    
    def choose_date(self):
        # 开始年份
        start_year_label = ttk.Label(self.left_top_frame, text="起始年:")
        start_year_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        self.start_year_combobox = ttk.Combobox(self.left_top_frame, values=list(range(2008, 2024)), state='readonly')
        self.start_year_combobox.set("年份(西元)")
        self.start_year_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        self.start_year_combobox.bind("<<ComboboxSelected>>", self.update_end_years)

        # 开始月份
        start_month_label = ttk.Label(self.left_top_frame, text="起始月:")
        start_month_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")
        self.start_month_combobox = ttk.Combobox(self.left_top_frame, values=[f'{i:02d}' for i in range(1, 13)], state='readonly')
        self.start_month_combobox.set("月份")
        self.start_month_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="W")
        self.start_month_combobox.bind("<<ComboboxSelected>>", self.update_end_months)

        # 结束年份
        end_year_label = ttk.Label(self.left_top_frame, text="結束年:")
        end_year_label.grid(row=3, column=0, padx=10, pady=10, sticky="W")
        self.end_year_combobox = ttk.Combobox(self.left_top_frame, state='readonly')
        self.end_year_combobox.set("年份(西元)")
        self.end_year_combobox.grid(row=3, column=1, padx=10, pady=10, sticky="W")

        # 结束月份
        end_month_label = ttk.Label(self.left_top_frame, text="結束月:")
        end_month_label.grid(row=4, column=0, padx=10, pady=10, sticky="W")
        self.end_month_combobox = ttk.Combobox(self.left_top_frame, values=[f'{i:02d}' for i in range(1, 13)], state='readonly')
        self.end_month_combobox.set("月份")
        self.end_month_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="W")

        # 閾值
        alpha_label = ttk.Label(self.left_top_frame, text="閾值:")
        alpha_label.grid(row=5, column=0, padx=10, pady=10, sticky="W")
        self.alpha_combobox = ttk.Combobox(self.left_top_frame, values=[f'{i/10:.1f}' for i in range(0, 11)], state='readonly')
        self.alpha_combobox.set("0.0")
        self.alpha_combobox.grid(row=5, column=1, padx=10, pady=10, sticky="W")

        ttk.Label(self.left_top_frame, text="stock_id").grid(row=0,column=0,padx=(10,10),pady=(10,10))
        ttk.Entry(self.left_top_frame, textvariable=self.stock_id_var).grid(row=0,column=1,padx=(10,10),pady=(10,10))
        ttk.Button(self.left_top_frame,text="送出",command=self.update_stock_id).grid(row=6,column=1,sticky="se")

    def update_end_years(self, event):
        start_year = int(self.start_year_combobox.get())
        self.end_year_combobox['values'] = list(range(start_year, 2024))
        self.end_year_combobox.set("年份(西元)")

    def update_end_months(self, event=None):
        start_year = int(self.start_year_combobox.get())
        start_month = int(self.start_month_combobox.get())

        if start_month == "月份":
            return
        if self.end_year_combobox.get() != "年份(西元)":
            if (start_year == int(self.end_year_combobox.get())) and self.end_year_combobox.get() != "年份(西元)":  # 如果开始年份等于结束年份
                self.end_month_combobox['values'] = [f'{i:02d}' for i in range(start_month , 13)]
                self.end_month_combobox.set(f'{start_month :02d}')
            else:
                self.end_month_combobox['values'] = [f'{i:02d}' for i in range(1, 13)]
                self.end_month_combobox.set("月份")

    def update_stock_id(self):
        try:
            self._stock_id = int(self.stock_id_var.get())
            start_year = self.start_year_combobox.get()
            start_month = self.start_month_combobox.get()
            end_year = self.end_year_combobox.get()
            end_month = self.end_month_combobox.get()

            if (start_year == "年份(西元)" or start_month == "月份" or
                end_year == "年份(西元)" or end_month == "月份"):
                messagebox.showinfo("Input Error", "Please select both start and end dates.")
            else:
                self.clean_right()
                self.main(start_year, start_month, end_year, end_month)

        except ValueError:
            print("Invalid stock ID input")

    def main(self,start_year, start_month, end_year, end_month):
        stock_id=self.stock_id
        file_path='data.csv'

        month_datas=pd.DataFrame()
        original_datas=pd.DataFrame()
        #檢查是否檔案下載了
        if rdata.Check_Data_Csv():
            print("csv 已經存在")
            month_datas = pd.read_csv(file_path)
        else:
            print("下載檔案")
            original_datas:pd.DataFrame=rdata.Get_N_Month_Data(stock_id=stock_id,
                                                               start_year=start_year,start_month=start_month,
                                                               end_year=end_year,end_month=end_month)
            
            #將該網站的日期從str -> datetime
            # month_datas['日期'] = month_datas['日期'].apply(datas.parse_custom_date)

            #特徵值使用
            window=20
            original_datas = Feature().Calculate_Moving_Average(data=original_datas, window=window)
            original_datas = Feature().Calculate_Rsi(data=original_datas,window=window)

            num_std=2
            original_datas=Feature().Calculate_Bollinger_Bands(data=original_datas,window=window,num_std=num_std)
            original_datas = Feature()._Calculate_Macd(original_datas)
            #丟33筆
            original_datas:pd.DataFrame = original_datas.iloc[33:]
            #去除離群值
            # for column in original_datas.columns:
            #     n=1.5
            #     IQR = np.percentile(original_datas[column],75) - np.percentile(original_datas[column],25)
            #     original_datas=original_datas[original_datas[column] < np.percentile(original_datas[column],75)+n*IQR]
            #     #outlier = Q1 - n*IQR
            #     original_datas=original_datas[original_datas[column] > np.percentile(original_datas[column],25)-n*IQR]

            #將close 改到最後面
            cols = original_datas.columns.tolist()
            cols.append(cols.pop(cols.index('Close')))
            original_datas = original_datas[cols]

            month_datas = original_datas.drop(columns=['Date'])
            original_datas.to_csv('2330.csv', index=False)
            # 將 month_datas 寫入 data.csv
            month_datas.to_csv('data.csv', index=False)

        self._stock_data=month_datas
        self.feature_extraction()
        self.boxplot_features(0,self._stock_data.columns)
        self.distplot_features(1,self._stock_data.columns)
        # self.create_checkbuttons()
        selected_features=self.get_selected_features()
        self.boxplot_features(2,selected_features[0:6])
        self.distplot_features(3,selected_features[0:6])

    def feature_extraction(self):

        choose_function_label = ttk.Label(self.left_bottom_frame, text="特徵選擇方法:")
        choose_function_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.choose_function_combobox = ttk.Combobox(self.left_bottom_frame, values=['pearson','kendall','spearman'], state='readonly')
        self.choose_function_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        self.choose_function_combobox.bind("<<ComboboxSelected>>", self.plot_heatmap)

    def plot_heatmap(self, event=None):
        selected_method = event.widget.get()
        if not selected_method:
            return
        
        corr_matrix = self._stock_data.corr(method=selected_method.lower())

        # Create a figure and plot the heatmap
        fig = plt.Figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 5}, ax=ax)
        ax.set_title(f'Correlation Heatmap (Method: {selected_method})')

        # Embed the plot in a tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=self.left_bottom_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0,padx=10, pady=10, sticky="W")

        # Update canvas scroll region
        canvas.get_tk_widget().bind("<Configure>", lambda e: canvas.get_tk_widget().configure(scrollregion=canvas.get_tk_widget().bbox("all")))

    def create_checkbuttons(self):
        for widget in self.left_bottom_frame.winfo_children():
            widget.destroy()

        check_vars = []
        features = self._stock_data.keys()
        for i, feature in enumerate(features):
            var = tkinter.BooleanVar()
            checkbutton = ttk.Checkbutton(self.left_bottom_frame, text=feature, variable=var)
            checkbutton.grid(row=i, column=0, sticky="w")
            check_vars.append((feature,var))

        ttk.Button(self.left_bottom_frame,text="確認",command=self.choosen_features).grid(row=len(features), column=0, sticky="w")

        self._stock_features=check_vars

    def choosen_features(self):
        self.boxplot_features()
        self.distplot_features()

    def get_selected_features(self):

        alpha=float(self.alpha_combobox.get())

        data_x = self._stock_data.iloc[:, :-1]
        data_y = self._stock_data.iloc[:, -1]
        n = 16
        chi = SelectKBest(f_regression, k=n)
        arrchi = chi.fit_transform(data_x, data_y)
        score = np.round(chi.scores_,4)
        selected_scores = score[np.abs(score) > alpha]
        scoresort = np.argsort(selected_scores)
        scoresort = np.flipud(scoresort)
        col = self._stock_data.columns

        return col[scoresort]
    
    def clean_right(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    #畫盒鬚圖
    def boxplot_features(self,index,selected_features):
        
        for i, fea in enumerate(selected_features):
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.boxplot(self._stock_data[fea], showmeans=True)
            ax.set_title(fea)

            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=index, column=i, sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    #畫常態圖
    def distplot_features(self,index,selected_features):

        for i, fea in enumerate(selected_features):
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.distplot(self._stock_data[fea], ax=ax, hist=True, kde=True, rug=False, bins=20,
                         hist_kws={'edgecolor': 'black'}, kde_kws={'linewidth': 2})
            ax.set_title(fea)

            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=index, column=i, sticky="nsew")
            self.scrollable_frame.grid_rowconfigure(i, weight=1)

    
        