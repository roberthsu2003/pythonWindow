import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

t = [2022, '楊志龍','ACN','中信',40,0,40,0,0,0,2,4,0,12,37.0,158,628,31,0,16,0,4,42,4,0,20,17,34,31,2022,'右投右打',56,'189(CM) / 102(KG)'
     ,'1993/04/07','https://www.cpbl.com.tw/files/atts/0L087782012129886612/56楊志龍.jpg',10.22,4.14]

t = [2022, '請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員','請選擇球員']

class cpblTreeView(ttk.Treeview):

    def __init__(self,parent,**kwargs):   
        super().__init__(parent,**kwargs) 
        self.parent = parent
        self.heading('Year', text="年份")
        self.heading('Team Name', text="所屬球隊")
        self.heading('ID', text="球員編號")
        self.heading('Name', text="球員姓名")
        self.heading('G', text="出場數")
        self.heading('GS', text="先發次數")
        self.heading('GR', text="中繼次數")
        self.heading('W', text="勝場數")
        self.heading('L', text="敗場數")
        self.heading('SV', text="救援成功")
        self.heading('HLD', text="中繼成功")
        self.heading('IP', text="有效局數")
        self.heading('BF', text="面對打者數")
        self.heading('H', text="被安打數")
        self.heading('HR', text="被全壘打數")
        self.heading('BB', text="保送數")
        self.heading('SO', text="三振數")
        self.heading('ER', text="自責分")
    
    #--------------設定欄位寬度-----------------------
        self.column('Year',width=70,anchor='center') 
        self.column('Team Name',width=70,anchor='center')
        self.column('ID',width=100,anchor='center')
        self.column('Name',width=70,anchor='center')
        self.column('G',width=70,anchor='center')
        self.column('GS',width=70,anchor='center')
        self.column('GR',width=70,anchor='center')
        self.column('W',width=70,anchor='center')
        self.column('L',width=70,anchor='center')
        self.column('SV',width=70,anchor='center')
        self.column('HLD',width=70,anchor='center')
        self.column('IP',width=70,anchor='center')
        self.column('BF',width=70,anchor='center')
        self.column('H',width=70,anchor='center')
        self.column('HR',width=70,anchor='center')
        self.column('BB',width=70,anchor='center')
        self.column('SO',width=70,anchor='center')
        self.column('ER',width=70,anchor='center')

    #--------------bind button1-------------------------
        self.bind('<ButtonRelease-1>',self.selectionItem)
        

    #-------------更新資料內容------------------------
    def update_content(self,site_datas):
        #必須先清除所有內容
        for i in self.get_children():
            self.delete(i)
        
        for index, site in enumerate(site_datas):
            self.insert('','end',text=f'abc{index}' ,values=site)
        

    #點擊treeView時，啟動此方法，回傳使用者點擊資料
    def selectionItem(self, event)->list:
       global t
       selectedItem = self.focus()
       data_dict = self.item(selectedItem)
       t = data_dict['values']
       print(f'selectionItem查詢結果{t}')

class player():
    #回傳使用者姓名，抓取照片檔名
    @staticmethod
    def player_name():
        player_name_list = t[3]
        return player_name_list
    
    #回傳球員詳細資料
    @staticmethod
    def list_info():
        global t
        print(f'list_info{t}')
        player_info = t
        return player_info
    
    #計算奪三振率及ERA平均，並抓取球員數值製作圖表
    @staticmethod
    def k9_era():
        def calculate_k9(so, ip):
            try:
                k9 = (so / ip) * 9
                return round(k9, 2)
            except ZeroDivisionError:
                return 0.0

        def calculate_era(er, ip):
            try:
                era = (er * 9) / ip
                return round(era, 2)
            except ZeroDivisionError:
                return 0.0

        #讀取csv檔案
        cpbl_pitchings_csv = 'pitchings_2022_updated.csv'

        # 初始化變數以保存平均值
        total_k9 = 0.0
        total_era = 0.0
        count = 0

        with open(cpbl_pitchings_csv, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                so = float(row['SO'])
                ip = float(row['IP'])
                er = float(row['ER'])

                k9 = calculate_k9(so, ip)
                era = calculate_era(er, ip)

                total_k9 += k9
                total_era += era
                count += 1

        # 計算平均值
        average_k9 = round((total_k9 / count if count > 0 else 0.0), 2)
        average_era = round((total_era / count if count > 0 else 0.0), 2)

        print(f'平均 K9: {average_k9}')
        print(f'平均 ERA: {average_era}')

        return average_k9, average_era

    
    @staticmethod
    def pr_value(container):
        global t
        data = t

        #檢查傳入的值長度是否正確
        if len(data) >= 20:
            k9_value = data[23]
            era_value = data[24]

            try:
                k9_values = float(k9_value)
                era_values = float(era_value)
            except ValueError:
                print("無法將 K9 或 ERA 值轉換為浮點數。")
                return

            # 設定 Matplotlib 樣式
            plt.style.use('dark_background')

            fig, ax = plt.subplots(figsize=(1.3, 1.3))
            #ax.set_yticks([])

            # 繪製長條圖
            sns.barplot(x=['K9', 'ERA'], y=[k9_values, era_values], errorbar=None, ax=ax, color='#0F4C3A',width=0.5)
            sns.despine(top = True, right = True, left=True, bottom=True) # 移除上方跟右方的框線
            
            # 在長條上顯示 y 值
            for i, value in enumerate([k9_values, era_values]):
                ax.text(i, value, f'{value:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=5, color='white')

            # 叫出平均值
            average_k9, average_era = player.k9_era()

            # 加入平均線
            ax.axhline(average_k9, color='#66BAB7', linestyle='dashed', linewidth=1, label='Average K9')
            ax.axhline(average_era, color='#B1B479', linestyle='dashed', linewidth=1, label='Average ERA')

            # 顯示索引方塊
            plt.legend(labels=["average_k9", "average_era"], loc='lower left',fontsize=5)

            # 調整 x 和 y 軸上的標籤大小
            ax.tick_params(axis='x', labelsize=5)
            ax.tick_params(axis='y', labelsize=5)

            # 建立FigureCanvasTkAgg及設定放置容器
            canvas = FigureCanvasTkAgg(fig, master=container)
            canvas.draw()

            #建立canvas繪製容器並打包至容器中
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side='left', fill='both', expand=True)

            return canvas
        else:
            print("資料錯誤，請重新選取")