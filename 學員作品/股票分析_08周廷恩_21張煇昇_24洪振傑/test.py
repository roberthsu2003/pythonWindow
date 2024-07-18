import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import numpy as np       #數學處理
import pandas as pd
import matplotlib.pyplot as plt #繪圖
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as mticker
import seaborn as sns
from sklearn.feature_selection import SelectKBest,f_regression
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

class App(ThemedTk):
    def __init__(self):
        super().__init__()
        self._stock_data = {}  # 用字典保存不同代號的 DataFrame
        self.set_theme("arc")  # 設置主題為 "arc"
        self.title("股票預測專案")
        self.geometry("800x900")

        self.tab_control = ttk.Notebook(self)
        self.tab_control.grid(row=0, column=0, sticky="nsew")

        self.tabs = {}  # 用於保存每個標籤頁和其關閉按鈕
        self.input_numbers = []  # 保存輸入的代號

        self.create_initial_tab()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_initial_tab(self):
        initial_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(initial_tab, text="首頁")
        
        label = ttk.Label(initial_tab, text="台灣股票代號")
        label.grid(row=0, column=0, sticky="w", padx=5)

        self.input_field = ttk.Entry(initial_tab)
        self.input_field.grid(row=0, column=1, sticky="ew", pady=5)
        
        add_button = ttk.Button(initial_tab, text="ADD", command=self.submit_inputs)
        add_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        self.number_list_frame = ttk.Frame(initial_tab)
        self.number_list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        
    def submit_inputs(self):
        input_value = self.input_field.get()
        if input_value:  # 確保輸入框不為空
            self.input_numbers.append(input_value)
            self.input_field.delete(0, tk.END)
            self.update_number_list()

    def update_number_list(self):
        for widget in self.number_list_frame.winfo_children():
            widget.destroy()


        for number in self.input_numbers:
            number_label = ttk.Label(self.number_list_frame, text=number, cursor="hand2")
            number_label.grid(sticky="ew")
            
            # number_label.bind("<Button-1>", lambda e, num=number: self.display_data(num))
            tree_columns = ['Date','Open', 'High', 'Low', 'Close', 'Volume']
            tree = ttk.Treeview(self.number_list_frame, columns=list(tree_columns),height=0, show='headings')
            tree.grid(sticky="nsew")

            data=self.display_data(number)
            if data is None:
                data = pd.DataFrame(columns=tree_columns)

            # 设置 Treeview 标头及宽度
            for col in tree_columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='center')

            first_row = data[tree_columns].iloc[::-1].iloc[0]
            formatted_row = [first_row['Date']] + [f"{value:.4f}" for value in first_row[1:]]
            tree.insert("", "end", values=formatted_row)

            tree.bind("<Double-1>", lambda e, num=number: self.create_new_tab(num,data))

    def display_data(self, number):
        # 讀取對應的 CSV 文件
        if (number not in self._stock_data):
            try:
                self._stock_data[number] = pd.read_csv(f'{number}.csv')
            except FileNotFoundError:
                print(f"文件 {number}.csv 未找到")
                return 

        df = self._stock_data[number]
        

        return df

    def create_new_tab(self, tab_name, data: pd.DataFrame):
        new_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(new_tab, text=tab_name)

        top_frame = ttk.Frame(new_tab, padding=20)
        top_frame.grid(row=1, column=0, sticky="nsew")
        new_tab.grid_rowconfigure(1, weight=1)
        new_tab.grid_columnconfigure(0, weight=1)

        label = ttk.Label(top_frame, text=f"這是 {tab_name} 的內容")
        label.grid(row=0, column=0, sticky="w")

        describe_button = ttk.Button(top_frame, text="敘述統計", command=lambda: self.show_describe_stats(data))
        describe_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")  # 适当设置 padx 和 pady

        nodate_datas = data.drop(columns=['Date'])
        heat_map_button = ttk.Button(top_frame, text="熱力圖", command=lambda: self.show_heat_map(nodate_datas))
        heat_map_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        feature_check_button = ttk.Button(top_frame, text="特徵驗證", command=lambda: self.feature_check(nodate_datas))
        feature_check_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        Bottom_frame = ttk.Frame(new_tab, padding=20)
        Bottom_frame.grid(row=2, column=0, sticky="nsew")

        self.candlestick_chat_graph(data, Bottom_frame)
        self.macd_graph(data, Bottom_frame)

        tab_id = self.tab_control.index("end") - 1

        tab_title_frame = ttk.Frame(new_tab)
        tab_title_frame.grid(row=0, column=0, sticky="ew")

        tab_label = ttk.Label(tab_title_frame, text=tab_name)
        tab_label.grid(row=0, column=0, sticky="w")

        close_button = ttk.Label(tab_title_frame, text=" ✖", foreground="red", cursor="hand2")
        close_button.grid(row=0, column=1, sticky="e")
        close_button.bind("<Button-1>", lambda e, tab_id=tab_id: self.close_tab(tab_id))

        self.tabs[tab_id] = {"frame": new_tab, "title_frame": tab_title_frame, "button": close_button}

        self.tab_control.select(new_tab)

    def candlestick_chat_graph(self,data,frame):
        # 创建 matplotlib 图形
        fig, ax = plt.subplots(figsize=(5, 3))

        # 绘制 K 线图
        for index, row in data.iterrows():
            date = row['Date']
            open_price = row['Open']
            close_price = row['Close']
            high_price = row['High']
            low_price = row['Low']

            if close_price >= open_price:
                # 涨：最高价 - 收盘价 和 开盘价 - 最低价 的填充为红色
                ax.fill([date, date, date], [high_price, close_price, open_price], 'red', edgecolor='red', linewidth=2, alpha=0.3)
                ax.plot([date, date], [low_price, high_price], color='black', linewidth=1)
            else:
                # 跌：最高价 - 开盘价 和 收盘价 - 最低价 的填充为绿色
                ax.fill([date, date, date], [high_price, open_price, close_price], 'green', edgecolor='green', linewidth=2, alpha=0.3)
                ax.plot([date, date], [low_price, high_price], color='black', linewidth=1)

        # 绘制折线图
        ax.plot(data['Date'], data['upperband'], marker='', color='blue', linewidth=1, linestyle='--', label='Upper Band')
        ax.plot(data['Date'], data['ma'], marker='', color='black', linewidth=1, label='Price (MA)')
        ax.plot(data['Date'], data['lowerband'], marker='', color='red', linewidth=1, linestyle='--', label='Lower Band')

        # 设置标题和标签
        ax.set_title('K线图与折线图')
        ax.set_xlabel('日期')
        ax.set_ylabel('Price')

        # 添加图例
        ax.legend()
        
        # x 軸處理
        tick_spacing = data['Date'].size/12 # x軸密集度
        ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))

        # 自动调整日期显示格式
        fig.autofmt_xdate()

        # 将 matplotlib 图形嵌入到 tkinter 中
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def macd_graph(self,data,frame):
        fig, ax = plt.subplots(figsize=(5, 3))


        # 繪製快速線（MACD line），紅色
        ax.plot(data['Date'], data['MACD'], color='red', label='MACD')

        # 繪製信號線（Signal line），黃色
        ax.plot(data['Date'], data['Signal_Line'], color='yellow', label='Signal Line')

        # 繪製柱狀圖（Histogram），高為紅色，低為綠色
        ax.bar(data['Date'], data['MACD_Histogram'], width=0.7, color=np.where(data['MACD_Histogram'] >= 0, 'red', 'green'), alpha=0.7, label='MACD Histogram')

        # 添加圖表元素和標籤
        ax.set_title('MACD Chart for ')
        ax.set_xlabel('Date')
        ax.set_ylabel('MACD')

        # 添加图例
        ax.legend()
        
        # x 軸處理
        tick_spacing = data['Date'].size/12 # x軸密集度
        ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))

        # 自动调整日期显示格式
        fig.autofmt_xdate()

        # 将 matplotlib 图形嵌入到 tkinter 中
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def close_tab(self, tab_id):
        self.tab_control.forget(self.tabs[tab_id]["frame"])
        del self.tabs[tab_id]

    def show_describe_stats(self, data):
        top_window = tk.Toplevel(self)
        top_window.title("敘述統計")
        top_window.geometry("600x300")
        stats = data.describe()

        # 构建列名列表，加入空格作为第一列
        columns = [" "] + list(stats.columns)

        tree = ttk.Treeview(top_window, columns=columns, show="headings")
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 添加表头
        for col in stats.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center', stretch=False)

        # 插入数据
        for stat_type, row in stats.iterrows():
            values = [stat_type] + row.tolist() 
            tree.insert("", "end", values=values)

        # 添加垂直滚动条
        hscrollbar = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=hscrollbar.set)

    def show_heat_map(self, data):

        top_window = tk.Toplevel(self)
        top_window.title("特徵分析")
        top_window.geometry("600x500")

        heat_map_frame = ttk.Frame(top_window)
        heat_map_frame.grid(row=0, column=0, sticky="nsew")

        top_window.grid_rowconfigure(0, weight=1)
        top_window.grid_columnconfigure(0, weight=1)
        
        choose_function_label = ttk.Label(heat_map_frame, text="特徵選擇方法:")
        choose_function_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        self.choose_function_combobox = ttk.Combobox(heat_map_frame, values=['pearson', 'kendall', 'spearman'], state='readonly')
        self.choose_function_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        self.choose_function_combobox.bind("<<ComboboxSelected>>", lambda event: self.plot_heatmap(data, heat_map_frame, event))

        alpha_label = ttk.Label(heat_map_frame, text="閾值:")
        alpha_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.alpha_combobox = ttk.Combobox(heat_map_frame, values=[f'{i/10:.1f}' for i in range(0, 11)], state='readonly')
        self.alpha_combobox.set("0.0")
        self.alpha_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="W")
        self.alpha_combobox.bind("<<ComboboxSelected>>", lambda event: self.feature_extraction(data, event))

    def feature_extraction(self, data, event=None):
        if hasattr(self, 'top_window_feature'):
            self.top_window_feature.destroy()  # 销毁现有窗口（如果存在）

        self.top_window_feature = tk.Toplevel(self)
        self.top_window_feature.title("特徵結果")
        self.top_window_feature.geometry("600x500")

        feature_method = self.choose_function_combobox.get()
        features_corr = data.corr(method=feature_method)

        target_corr = features_corr['Close'].drop(index=['Close'])

        alpha = float(self.alpha_combobox.get())
        selected_features = target_corr[abs(target_corr) > alpha].sort_values(ascending=False)

        tree = ttk.Treeview(self.top_window_feature, columns=["Feature", "Correlation"], show="headings")
        tree.heading("Feature", text="特徵名稱")
        tree.heading("Correlation", text="相關係數")
        tree.pack(fill=tk.BOTH, expand=True)

        for feature, correlation in selected_features.items():
            tree.insert("", "end", values=[feature, correlation])

    def plot_heatmap(self, data ,frame,event=None):
        selected_method = event.widget.get()
        if not selected_method:
            return

        corr_matrix = data.corr(method=selected_method)

        # Create a figure and plot the heatmap
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 5}, ax=ax)
        ax.tick_params(axis='both', which='major', labelsize=5)
        ax.set_title(f'Correlation Heatmap (Method: {selected_method})')

        # Embed the plot in a tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1,padx=10, pady=10, sticky="nsew")

        # Update canvas scroll region
        canvas.get_tk_widget().bind("<Configure>", lambda e: canvas.get_tk_widget().configure(scrollregion=canvas.get_tk_widget().bbox("all")))

    def feature_check(self, data):
        top_window = tk.Toplevel(self)
        top_window.title("特徵驗證")
        top_window.geometry("600x500")

        feature_check_frame = ttk.Frame(top_window)
        feature_check_frame.grid(row=0, column=0, sticky="ew")
        
        feature_check_combobox = ttk.Combobox(feature_check_frame, values=['f_regression'], state='readonly')
        feature_check_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="W")
        feature_check_combobox.bind("<<ComboboxSelected>>", lambda event: self.feature_score(data, feature_check_frame, event))
        
        
    def feature_score(self,data,frame,event=None):

        df = data.iloc[:, :-1]
        target = data.iloc[:, -1]

        n = 16
        selected_method = event.widget.get()
        if selected_method == 'f_regression':
            chi = SelectKBest(f_regression, k=n)
        elif selected_method == 'chi2':
            chi = SelectKBest(chi2, k=n)
        chi.fit(df, target)

        score = abs(chi.scores_)
        scoresort = np.argsort(score)
        scoresort = np.flipud(scoresort)

        col = df.columns
        tree = ttk.Treeview(frame, columns=["Feature", "Score"], show="headings")
        tree.heading("Feature", text="特徵名稱")
        tree.heading("Score", text="相關係數分數")
        tree.grid(row=1, column=1, padx=10, pady=10, sticky="W")

        for idx in scoresort[:5]:
            feature = col[idx]
            correlation = score[idx]
            tree.insert("", "end", values=[feature, correlation])

    #畫盒鬚圖
    def boxplot_features(self,selected_features):
        
        for i, fea in enumerate(selected_features):
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.boxplot(self._stock_data[fea], showmeans=True)
            ax.set_title(fea)

            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=i, sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    #畫常態圖
    def distplot_features(self,selected_features):

        for i, fea in enumerate(selected_features):
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.distplot(self._stock_data[fea], ax=ax, hist=True, kde=True, rug=False, bins=20,
                         hist_kws={'edgecolor': 'black'}, kde_kws={'linewidth': 2})
            ax.set_title(fea)

            canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=i, sticky="nsew")
            self.scrollable_frame.grid_rowconfigure(i, weight=1)

if __name__ == "__main__":

    def on_closing():
        app.destroy()
        app.quit()

    app = App()
    app.protocol("WM_DELETE_WINDOW",on_closing)
    app.mainloop()
