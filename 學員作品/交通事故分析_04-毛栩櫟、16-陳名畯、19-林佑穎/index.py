import tkinter as tk
from tkinter import ttk, messagebox
import platform     #配合不同作業系統的顯示字體
import matplotlib.pyplot as plt  # Import Matplotlib
from tkintermapview import TkinterMapView
import pandas as pd

class Window(tk.Tk):
   
    def __init__(self):
        super().__init__()
        self.title("交通事故資料查詢系統")
        self.geometry("1280x900")  

        self.init_vars()
        self.setup_gui()
        
    def init_vars(self):
        self.years = list(range(2018, 2025))
        self.months = list(range(1, 13))
        self.days = list(range(1, 32))

        # 設定縣市資料的資料表
        self.cities = ["臺北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "臺中縣", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"]

        # 設定天氣與光線的資料表
        self.weathers = ["晴", "陰", "雨"]
        self.lights = ["日間自然光線", "夜間(或隧道)有照明", "有照明且開啟", "無照明", "晨或暮光", "夜間(或隧道)無照明", "有照明未開啟或故障"]

        # 設定過濾器的變數值
        self.city_vars = {city: tk.BooleanVar() for city in self.cities}
        self.weather_vars = {weather: tk.BooleanVar(value=True) for weather in self.weathers}
        self.light_vars = {light: tk.BooleanVar(value=True) for light in self.lights}
        self.run_vars = {"是": tk.BooleanVar(value=True), "否": tk.BooleanVar(value=True)}

    def setup_gui(self):
        #主頁面設定
        mainframe = ttk.Frame(self)
        mainframe.pack(expand=True, fill='both', padx=10, pady=10)

        left_top_frame = ttk.Labelframe(mainframe, text="查詢條件")
        left_top_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.NW)

        date_frame = ttk.Labelframe(left_top_frame, text="日期")
        date_frame.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.setup_date_widgets(date_frame)

        city_frame = ttk.Labelframe(left_top_frame, text="縣市：")
        city_frame.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        self.setup_city_widgets(city_frame)

        extra_frame = ttk.Labelframe(left_top_frame, text="進階選項：")
        extra_frame.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
        self.setup_extra_widgets(extra_frame)

        #設定送出篩選按鈕及結果數目顯示
        self.submit_frame = ttk.Labelframe(left_top_frame, text="篩選結果：")
        self.submit_frame.grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self.submit_frame, text=f"案件數目：").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        submit_button=ttk.Button(left_top_frame, text="送出", command=self.submit_data).grid(column=0, row=4, padx=10, pady=10, sticky=tk.E)
        
        right_top_frame = ttk.Labelframe(mainframe, text="事故地圖")
        right_top_frame.grid(column=1, row=0, padx=10, pady=10)
        self.setup_map(right_top_frame)

        bottom_frame = ttk.Labelframe(mainframe, text="事故資料")
        bottom_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        self.setup_treeview(bottom_frame)

    def setup_date_widgets(self, parent):
        self.year = ttk.Combobox(parent, values=self.years, width=5, state="readonly")
        self.year.set(self.years[0])
        self.year.grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(parent, text="年").grid(column=1, row=0, padx=5, pady=5, sticky=tk.E)
        self.month = ttk.Combobox(parent, values=self.months, width=5, state="readonly")
        self.month.set(self.months[0])
        self.month.grid(column=2, row=0, padx=5, pady=5)
        ttk.Label(parent, text="月").grid(column=3, row=0, padx=5, pady=5, sticky=tk.E)
        self.day = ttk.Combobox(parent, values=self.days, width=5, state="readonly")
        self.day.set(self.days[0])
        self.day.grid(column=4, row=0, padx=5, pady=5)
        ttk.Label(parent, text="日").grid(column=5, row=0, padx=5, pady=5, sticky=tk.E)
        #設定日期按鈕自動變動
        self.year.bind("<<ComboboxSelected>>", self.update_dates)
        self.month.bind("<<ComboboxSelected>>", self.update_dates)
        self.day.bind("<<ComboboxSelected>>", self.update_dates)

    def setup_city_widgets(self, parent):
        self.select_all_button = ttk.Button(parent, text="全選", command=self.select_all)
        self.select_all_button.grid(column=0, row=0,columnspan=1, padx=5, pady=5, sticky=tk.W)
        for i, city in enumerate(self.cities):
            cb = ttk.Checkbutton(parent, text=city, variable=self.city_vars[city])
            cb.grid(column=i % 6, row=i // 6+1, padx=5, pady=5, sticky=tk.W)

    def setup_extra_widgets(self, parent):
        # 天气
        ttk.Label(parent, text="天候：").grid(column=0, row=0, padx=5, pady=5, sticky=tk.E)
        for i, weather in enumerate(self.weathers):
            ttk.Checkbutton(parent, text=weather, variable=self.weather_vars[weather]).grid(column=i + 1, row=0, padx=5, pady=5, sticky=tk.W)
        
        # 灯光
        ttk.Label(parent, text="光線：").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        for i, light in enumerate(self.lights):
            column = i % 3 + 1
            row = i // 3 + 1  # Start from row 2 to leave row 1 empty
            ttk.Checkbutton(parent, text=light, variable=self.light_vars[light]).grid(column=column, row=row, padx=5, pady=5, sticky=tk.W)

            
    def setup_map(self, parent):
        self.map = TkinterMapView(parent, width=600, height=400)
        self.map.grid(column=0, row=0, padx=10, pady=10)
        self.map.set_position(25.115045154785246, 121.53834693952264,marker=True)

        self.pie_chart_button = ttk.Button(parent, text="顯示对应的线图", command=self.show_charts)
        self.pie_chart_button.grid(column=0, row=1, padx=10, pady=10)

    def setup_treeview(self, parent):
        self.treeview = ttk.Treeview(parent, columns=('#0','#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8','#9'),show='headings')
        self.treeview.grid(column=0, row=0, sticky='nsew')
        #設定下方資料表單
        headings = ['發生日期', '發生時間', '事故類別', '發生地點', '天氣', '光線名稱','速限', '道路類別','事故類型','死亡受傷人數']
        for i, col in enumerate(headings,start=1):
            self.treeview.heading('#' + str(i), text=col, anchor='center')
            self.treeview.column('#' + str(i), minwidth=60, width=120, anchor='s')
        #設定資料表單滾動軸
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.treeview.yview)
        scrollbar.grid(column=1, row=0, sticky='ns')
        self.treeview.configure(yscrollcommand=scrollbar.set)

   
    def submit_data(self):
        selected_year = self.year.get()
        selected_month = int(self.month.get())
        selected_day = int(self.day.get())
        selected_cities = [city for city, var in self.city_vars.items() if var.get()]
        selected_weathers = [weather for weather, var in self.weather_vars.items() if var.get()]
        selected_lights = [light for light, var in self.light_vars.items() if var.get()]
        #讀取檔案
        try:
            df=pd.read_csv(f"./data/{selected_year}.csv",encoding='utf-16')
            df.columns=df.columns.str.strip()
        except FileNotFoundError:
            messagebox.showerror(f"找不到{selected_year}.csv資料")
        df['發生日期']=pd.to_datetime(df['發生日期'])
        df['month']=df['發生日期'].dt.month
        df['day']=df['發生日期'].dt.day
        #利用pandas功能篩選資料
        filtered_df = df[
            (df['month'] == selected_month) &
            (df['day'] == selected_day) &
            (df['發生地點'].isin(selected_cities)) &
            (df['天候名稱'].isin(selected_weathers)) &
            (df['光線名稱'].isin(selected_lights)) 
        ]
        result_count = len(filtered_df)
        self.update_counts(result_count)
        self.populate_respond(filtered_df)
    
    #自動資料數目計算刷新功能
    def update_counts(self,count):
        for widget in self.submit_frame.winfo_children():   
            widget.destroy()
        ttk.Label(self.submit_frame, text=f"案件數目：{count}").grid(column=1, row=0, padx=10, pady=10, sticky=tk.W)
        
    def populate_respond(self,data):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        #整理日期與時間資料型態
        for _, row in data.iterrows():
            formatted_time=row['發生時間'].split('.')[0]
            formatted_date=row['發生日期'].strftime('%Y-%m-%d')

        #讀取資料
            self.treeview.insert('','end', values=(
                formatted_date,
                formatted_time,
                row['事故類別名稱'],
                row['發生地點'],
                row['天候名稱'],
                row['光線名稱'],
                row['速限_第1當事者'],
                row['道路類別_第1當事者_名稱'],
                row['事故類型及型態大類別名稱'],
                row['死亡受傷人數']
            ))

        #將讀取資料匯入地圖
        self.map.delete_all_marker()
        for _, row in data.iterrows():
            lat=float(row['緯度'])
            lng=float(row['經度'])
            self.map.set_position(lat,lng,marker=True)
            
    def update_dates(self, event=None):
        year = int(self.year.get())
        month = int(self.month.get())
        day = int(self.day.get())
        if year == 2024:
            self.month['values']=list(range(1,7))
            if month>6:
                self.month.set(6)
        else:
            self.month['values']=list(range(1,13))
        
        if month == 2 and (year == 2020 or year==2024):
            self.day['values']=list(range(1,30))
            if day > 29:
                self.day.set(29)
        elif month == 2:
            self.day['values']=list(range(1,29))
            if day > 28:
                self.day.set(28)
        elif month in [4,6,9,11]:
            self.day['values']=list(range(1,31))
            if day > 30:
                    self.day.set(30)
        else:
            self.day['values']=list(range(1,32))

    def select_all(self):
        for var in self.city_vars.values():
            var.set(True)

    def get_treeview_data(self):
        data = []
        for row in self.treeview.get_children():
            data.append(self.treeview.item(row)['values'])
        columns = ['日期', '時間', '事故類別', '地區', '天氣', '光線狀態', '速限', '道路類別', '事故類型及型態大類別名稱','死亡受傷人數']
        df = pd.DataFrame(data, columns=columns)
        return df
    
    def show_charts(self):
        if platform.system() == 'Windows':      #Windows
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
        elif platform.system() == 'Darwin':   #macOS
            plt.rcParams['font.sans-serif'] = ['PingFang', 'STHeiti', 'Arial Unicode MS'] # 使用中文字體
        df = self.get_treeview_data()
        if df.empty:
            messagebox.showerror("錯誤","未選擇資料")
            return
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
        df['時間分類'] = df['時間'].apply(classify_time)
        weather_counts = df['天氣'].value_counts()
        axes[0,0].pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=90)
        axes[0,0].set_title('天候分佈')
        
        accident_type_counts = df['事故類型及型態大類別名稱'].value_counts()
        axes[0,1].bar(accident_type_counts.index, accident_type_counts.values, color='skyblue')
        axes[0,1].set_xlabel('事故類型')
        axes[0,1].set_ylabel('事件數')
        axes[0,1].set_title('交通事故類型分佈')
        axes[0,1].tick_params(axis='x')

        road_type_counts=df['道路類別'].value_counts()
        axes[1,0].bar(road_type_counts.index, road_type_counts.values, color='brown')
        axes[1,0].set_xlabel('道路類型')
        axes[1,0].set_ylabel('事件數')
        axes[1,0].set_title('道路類型分佈')
        axes[1,0].tick_params(axis='x')

        time_type_counts=df['時間分類'].value_counts()
        axes[1,1].pie(time_type_counts,labels=time_type_counts.index, autopct='%1.1f%%', startangle=90)
        axes[1,1].set_title('事故時間分佈')

        plt.tight_layout()  
        plt.show()

def classify_time(time_str):
    time = pd.to_datetime(time_str, format='%H:%M:%S').time()
    if time >= pd.to_datetime('08:00:00', format='%H:%M:%S').time() and time < pd.to_datetime('18:00:00', format='%H:%M:%S').time():
        return '白天'
    elif time >= pd.to_datetime('18:00:00', format='%H:%M:%S').time() or time < pd.to_datetime('04:00:00', format='%H:%M:%S').time():
        return '晚上'
    else:
        return '清晨'

if __name__ == "__main__":
    app = Window()
    app.mainloop()
