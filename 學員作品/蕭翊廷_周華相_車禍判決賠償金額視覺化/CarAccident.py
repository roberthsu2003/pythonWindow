import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd
import numpy as np
import csv
import subprocess


# 加入中文字型設定：Google-思源正黑體
fontManager.addfont('NotoSansTC-VariableFont_wght.ttf')
matplotlib.rc('font', family='Noto Sans TC')


# 設定全域變數
fig = None
fig_scatter = None
fig_barplot = None
fig_boxplot1 = None
ax = None
ax_scatter = None
ax_barplot = None
ax_boxplot1 = None
canvas = None
canvas_scatter = None
canvas_barplot = None
canvas_boxplot1 = None
text_box = None

# 創建圖表框


def create_frames(root):
    global fig, fig_scatter, fig_barplot, fig_boxplot1, ax, ax_scatter, ax_barplot, ax_boxplot1, canvas, canvas_scatter, canvas_barplot, canvas_boxplot1, text_box
    frames = {}
    for (x, y, z) in [(0,0,'圓餅圖'), (0,1,'直方圖'), (1,0,'統計資料'), (1,1,'箱形圖')]:
            frame = tb.Frame(root, borderwidth=2,
                             relief="solid", width=300, height=100)
            frame.grid(row=x, column=y, padx=3, pady=3)  # 添加間距
            label = tb.Label(frame, text=z, font=16)
            label.pack(padx=5,pady=(5,0))
            frame.configure(style='Blue.TFrame')
    # ------圓餅圖位置------
    frame_1_1 = root.grid_slaves(row=0, column=0)[0]
    fig, ax = plt.subplots(figsize=(4.5,3))  # 創建一個空的畫布
    ax.set_facecolor('none')
    canvas = FigureCanvasTkAgg(fig, master=frame_1_1)
    ax.set_facecolor('none')
    canvas.draw()
    canvas.get_tk_widget().pack(pady=9)
    canvas.get_tk_widget().pack_propagate(False)
    # ------長條圖位置------
    frame_1_2 = root.grid_slaves(row=0, column=1)[0]
    fig_barplot, ax_barplot = plt.subplots(figsize=(4.5,3))  # 創建一個空的畫布
    canvas_barplot = FigureCanvasTkAgg(
        fig_barplot, master=frame_1_2)
    canvas_barplot.draw()
    canvas_barplot.get_tk_widget().pack(pady=9)
    # ------text_box位置------
    frame_2_1 = root.grid_slaves(row=1, column=0)[0]
    # ------插入敘述性統計資料------
    text_box = tk.Text(frame_2_1, height=15, width=55,
                       bd=-1, font=(16), spacing3=5)
    text_box.pack()
    # ------盒鬚圖位置------
    frame_2_2 = root.grid_slaves(row=1, column=1)[0]
    fig_boxplot1, ax_boxplot1 = plt.subplots(figsize=(4.5,3))  # 創建一個空的畫布
    canvas_boxplot1 = FigureCanvasTkAgg(
        fig_boxplot1, master=frame_2_2)
    canvas_boxplot1.draw()
    canvas_boxplot1.get_tk_widget().pack(pady=9)


# ------讀取CSV檔，導入DataFrame------
df = pd.read_csv('10.csv')

# ------定義創建combobox的函式
def create_combobox(left_frame, label_text, values):
    label = tb.Label(left_frame, text=label_text)
    label.pack()
    combo_var = tk.StringVar()
    combobox = tb.Combobox(
        left_frame,
        textvariable=combo_var,
        values=values,
        state="readonly",
        style=SUCCESS
    )
    combobox.pack(fill='x', pady=5)
    combobox.current(0)
    return combo_var

# ------定義搜尋按鈕觸發動作函式------


def fetch_data():
    global df
    df1 = df  # 傳入全域變數df

    area = combo_var.get()
    period = combo_var1.get()
    many_p = combo_var2.get()
    many_d = combo_var3.get()

    condition1 = (df1['地區'] == area)
    condition2 = (df1['年月'] == period)
    condition3 = (df1['複數原告'] == many_p)
    condition4 = (df1['複數被告'] == many_d)

    if area != '全部案件':
        df1 = df1.loc[condition1]
    if period != '全部案件':
        df1 = df1.loc[condition2]
    if many_p != '全部案件':
        df1 = df1.loc[condition3]
    if many_d != '全部案件':
        df1 = df1.loc[condition4]

    df1 = df1[df1['總賠償金額'] != 0]

    # 將總賠償金額依金額大小排序
    df1 = df1.sort_values(by='總賠償金額', ascending=True, ignore_index=True)

    # 計算敘述性統計資料
    
    max = df1['總賠償金額'].max()
    min = df1['總賠償金額'].min()
    mean = df1['總賠償金額'].mean()
    median = df1['總賠償金額'].median()
    Q1 = df1['總賠償金額'].quantile(0.25)
    Q3 = df1['總賠償金額'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)
    outliers_above = df1[df1['總賠償金額'] > upper_bound]
    outliers_below = df1[df1['總賠償金額'] < lower_bound]
    count_above = len(outliers_above)

    # 將敘述性統計資料打包成字串
    textdata = f"最大值(MAX): {max}\n最小值(MIN): {min}\n平均值(MEAN): {mean}\n中位數(MEDIAN): {median}\n第一四分位數(Q1): {Q1}\n第三四分位數(Q3): {Q3}\n四分位距(IQR): {IQR}\n上邊界: {upper_bound}\n下邊界: {lower_bound}\n高於上邊界的數量: {count_above}"

    # 在 Text 组件中插入數據
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, textdata)

    # ------將篩選後的判決ID插入listbox
    new_values = df1['ID']
    listbox.delete(0, tk.END)  # 清除listbox內現有資料
    for value in new_values:
        listbox.insert(tk.END, value[:-11])
    ax.clear()

    # 獲取總賠償金額數據
    total_compensation = df1['總賠償金額']

    # 以ID為X軸
    IDname = df1['ID']
    colors = ['#2cbdfe', '#2fb9fc', '#33b4fa', '#36b0f8',
            '#3aacf6', '#3da8f4', '#41a3f2', '#449ff0',
            '#489bee', '#4b97ec', '#4f92ea', '#528ee8',
            '#568ae6', '#5986e4', '#5c81e2', '#607de0',
            '#6379de', '#6775dc', '#6a70da', '#6e6cd8',
            '#7168d7', '#7564d5', '#785fd3', '#7c5bd1',
            '#7f57cf', '#8353cd', '#864ecb', '#894ac9',
            '#8d46c7', '#9042c5', '#943dc3', '#9739c1',
            '#9b35bf', '#9e31bd', '#a22cbb', '#a528b9',
            '#a924b7', '#ac20b5', '#b01bb3', '#b317b1']

    # ------插入圓餅圖------
    ax.set_xticks([])
    explode = tuple(0.01 for _ in range(len(total_compensation)))
    ax.pie(total_compensation, explode=explode,
        autopct=None, startangle=90, colors=colors)
    ax.set_xlabel(None)
    ax.set_ylabel('總賠償金額')
    ax.grid(True)
    fig.tight_layout()
    canvas.draw()

    # ------插入長條圖------
    canvas_barplot.get_tk_widget().pack()
    ax_barplot.clear()
    ax_barplot.bar(IDname, total_compensation, color=colors)
    ax_barplot.set_xticks([])
    ax_barplot.set_yscale('log')  # 设置 Y 軸为對數尺度
    ax_barplot.set_xlabel(None)
    ax_barplot.set_ylabel('總賠償金額（對數變換）')
    ax_barplot.grid(True)
    fig_barplot.tight_layout()
    canvas_barplot.draw()


    # ------插入箱形圖------
    ax_boxplot1.clear()
    sns.boxplot(y=np.log10(df1['總賠償金額']), ax=ax_boxplot1, color='#894ac9')
    ax_boxplot1.grid(True)
    fig_boxplot1.tight_layout()
    canvas_boxplot1.draw()

# ------定義雙擊判決列表觸發動作函式------


def on_double_click(event):
    global df
    df2 = df  # 傳入全域變數df

    # ------取得選取項目的內容
    index = listbox.curselection()
    selected_item = listbox.get(index)

    # ------與DataFrame的ID欄位作模糊比對，得到PDF下載連結
    filt = (df2['ID'].str.startswith(selected_item))
    url_series = df2[filt]['PDF']
    url = url_series.iloc[0]

    try:
        filename = selected_item.replace(',', '_')  # 檔名中若有逗號會報錯
        filename = f'{filename}.pdf'
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as file:
            file.write(response.content)

        subprocess.Popen([filename], shell=True)  # 使用預設應用程式開啟PDF檔

    except:
        messagebox.showinfo(message='該判決無下載連結')


# ------創建視窗------
root = tb.Window(size=(1280, 768), position=(
    300, 200), resizable=(False, False), title='車禍判決賠償金額視覺化')

# ------創建左側邊框(控制面板)------
left_frame = tb.Frame(root,
                      padding=10,
                      borderwidth=2,
                      relief="solid",
                      width=300,
                      height=732)
left_frame.pack_propagate(False)  # 避免左側邊框自動縮小
left_frame.pack(side=LEFT,
                padx=(10, 0),
                pady=10)

# ------控制變量(地區、年月、原告、被告)combobox並傳回變數
regions = ['全部案件', '基隆', '台北', '新北', '桃園', '新竹', '苗栗', '台中', '南投',
           '彰化', '雲林', '嘉義', '台南', '高雄', '屏東', '宜蘭', '花蓮', '台東', '澎湖', '金門']
months = ['全部案件', '2022年01月', '2022年02月', '2022年03月', '2022年04月', '2022年05月', '2022年06月', '2022年07月', '2022年08月', '2022年09月',
          '2022年10月', '2022年11月', '2022年12月', '2023年01月', '2023年02月', '2023年03月', '2023年04月', '2023年05月', '2023年06月', '2023年07月']
options = ['全部案件', '是', '否']

combo_var = create_combobox(left_frame, "選擇地區", regions)
combo_var1 = create_combobox(left_frame, "選擇年月", months)
combo_var2 = create_combobox(left_frame, "複數原告", options)
combo_var3 = create_combobox(left_frame, "複數被告", options)

# ------搜尋按鈕------
tb.Button(left_frame,
          text='搜尋',
          bootstyle=(SUCCESS, OUTLINE),
          command=fetch_data).pack(pady=5)


# ------判決列表------
listbox_frame = tb.Frame(left_frame)
listbox_frame.pack(fill='x', pady=5)
scrollbar = tb.Scrollbar(listbox_frame)
scrollbar.pack(side='right', fill='y')
listbox = tk.Listbox(listbox_frame,
                     height=27,
                     yscrollcommand=scrollbar.set)
listbox.pack(fill='x', expand=True)
scrollbar.config(command=listbox.yview)

# ------綁定點擊事件------
listbox.bind("<Double-Button-1>", on_double_click)

# ------創建右側邊框(顯示圖表)------
right_frame = tb.Frame(root, padding=10, borderwidth=2,
                       relief="solid", width=700, height=748)
right_frame.pack(side=LEFT, padx=10, pady=10)
right_frame.pack_propagate(False)
create_frames(right_frame)

# ------確保視窗關閉時，程式能順利終止------


def on_closing():
    root.destroy()
    root.quit()


if __name__ == '__main__':
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
