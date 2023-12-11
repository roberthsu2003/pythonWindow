#-----匯入的模組-----#
import tkinter as tk
from tkinter import ttk
import json
import os
import csv
import yfinance as yf
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import sys


#-----下載個股價格-----#
def download_stock():
    stock_number=x.get()
    stock_data = yf.download(f'{stock_number}.tw', start='2022-1-1')
    stock_data.to_csv(f'{stock_number}.csv')
    stock = []
    with open(f'./{stock_number}.csv', 'r',  encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stock.append(row)
            with open(f'{stock_number}.json', 'w', encoding='utf-8') as file2:
                json.dump(stock, file2, ensure_ascii=False)
    with open(f'./{stock_number}.csv','r',encoding='utf-8') as file:
        data=pd.read_csv(file)
        round_data=round(data,ndigits=2)
        round_data.to_csv(f'./{stock_number}.csv',index=False)


#-----建立資料表-----#
def create_sql(conn):
    stock_number = x.get()
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE name='stock{stock_number}'")
    if cursor.fetchone():
        cursor.execute(f"DROP TABLE stock{stock_number}")
    cursor.execute(f"""
    CREATE TABLE stock{stock_number} (
        "id"	INTEGER,
	    "交易日"	INTEGER NOT NULL,
	    "開盤價"	INTEGER NOT NULL,
	    "當日最高價"	INTEGER NOT NULL,
	    "當日最低價"	INTEGER NOT NULL,
	    "收盤價"	INTEGER NOT NULL,
	    "調整後收盤價"	INTEGER NOT NULL,
	    "當日成交量"	INTEGER NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
        UNIQUE("交易日") ON CONFLICT REPLACE  
    );
    """)
    conn.commit()


# -----輸入資料表-----#
def insert_data(conn, values):
    stock_number = x.get()
    cursor = conn.cursor()
    sql = f"""
    INSERT INTO stock{stock_number}(交易日,開盤價,當日最高價,當日最低價,收盤價,調整後收盤價,當日成交量)
        VALUES(?,?,?,?,?,?,?)
    """
    cursor.execute(sql, values)
    conn.commit()


# -----寫入資料庫-----#
def update_data():
    stock_number = x.get()
    conn = sqlite3.connect('stock.db')
    download_stock()
    #treeview_stock()
    create_sql(conn)
    with open(f'{stock_number}.json', 'r', encoding='utf-8') as file:
        reader = json.load(file)
        for item in reader:
            insert_data(conn, [item['Date'], item['Open'], item['High'],
                        item['Low'], item['Close'], item['Adj Close'], item['Volume']])
    conn.commit()
    conn.close()


# -----顯示資料至treeview上-----#
def treeview_stock():
    stock_number=x.get()
    with open(f'{stock_number}.csv', 'r',  encoding='utf-8') as file:
        reader = csv.reader(file)
        reader = list(reader)
        for row in reversed(reader):
            tree.insert('','end',values=row)
    count_60()
    count_20()
    count_5()
    image()


# -----計算60日均值-----#
def count_60():
    stock_number=x.get()
    data = pd.read_csv(f'{stock_number}.csv')
    tail_60 = data.tail(60)
    save_60 = tail_60[["Date", "Close"]].to_csv('60day.csv')
    data_60 = pd.read_csv("60day.csv")
    close_60 = data_60["Close"]
    avg_60 = round(close_60.mean(),ndigits=2)
    sixty_60 = tk.Label(fouthFrame, text=f"60日均價={avg_60}", font=('細明體', 30))
    sixty_60.config(fg="black")
    sixty_60.pack(side="left",padx=10)


#-----計算20日均值-----#
def count_20():
    stock_number = x.get()
    data = pd.read_csv(f'{stock_number}.csv')
    tail_20 = data.tail(20)
    save_20 = tail_20[["Date", "Close"]].to_csv('20day.csv')
    data_20 = pd.read_csv("20day.csv")
    close_20 = data_20["Close"]
    avg_20 = round(close_20.mean(), ndigits=2)
    sixty_20 = tk.Label(fouthFrame, text=f"20日均價={avg_20}", font=('細明體', 30))
    sixty_20.config(fg="red")
    sixty_20.pack(side="left",padx=10)


# -----計算5日均值-----#
def count_5():
    stock_number = x.get()
    data = pd.read_csv(f'{stock_number}.csv')
    tail_5 = data.tail(5)
    save_5 = tail_5[["Date", "Close"]].to_csv('5day.csv')
    data_5 = pd.read_csv("5day.csv")
    close_5 = data_5["Close"]
    avg_5 = round(close_5.mean(), ndigits=2)
    sixty_5 = tk.Label(fouthFrame, text=f"5日均價={avg_5}", font=('細明體', 30))
    sixty_5.config(fg="black")
    sixty_5.pack(side="left",padx=10)


#-----產出圖片-----#
def image():
    data=pd.read_csv('60day.csv')
    tail=data.tail(60)
    mov5=data["Close"].rolling(window=5).mean()
    df_5=mov5.tail(60)
    df_5=df_5.to_list()
    mov20=data["Close"].rolling(window=20).mean()
    df_20=mov20.tail(60)
    df_20=df_20.to_list()
    mov60=data["Close"].rolling(window=60).mean()
    df_60=mov60.tail(60)
    df_60=df_60.to_list()
    plt.plot(df_5,color="#CB1B45")
    plt.plot(df_20,color="black")
    plt.savefig('mov.jpeg')


#-----線圖對話框-----#
def pop_up():
    os.system("python image.py")
#-----視窗設定-----#
Window=tk.Tk()
Window.title('個股資料查詢')
Window.geometry('1024x450')


#-----設定各個部位框架-----#
firstFrame=tk.Frame(Window) #第一部份的框架(下載股價)
firstFrame.pack()
secondFrame=tk.Frame(Window) #第二部份的框架(treeview顯示)
secondFrame.pack()
thirdFrame = tk.Frame(Window)  # 第三部份的框架(計算均價按鈕)
thirdFrame.pack()
fouthFrame=tk.Frame(Window) #第四部份的框架(顯示均價)
fouthFrame.pack()
fifthFrame=tk.Frame(Window) #第五部份的框架(設定跳出線圖對話框)
fifthFrame.pack()
sixthFrame=tk.Frame(Window) #第六部份的框架(顯示圖片)
sixthFrame.pack()


#-----第一部份框架內容-----#
x=tk.StringVar()
topic_label=tk.Label(firstFrame,text='個股查詢',font=('細明體',30))
topic_label.pack()
#-----設定搜尋股票代號-----#
entry_number=tk.Entry(firstFrame,textvariable=x)
entry_number.pack()
download_buttom = tk.Button(firstFrame, text='下載個股資料', command=update_data)
download_buttom.pack()


#-----第二部份框架內容-----#
display=tk.Button(secondFrame,text='顯示個股價格及均價',command=treeview_stock)
display.pack()
tree = ttk.Treeview(
    secondFrame, show="headings", columns=["日期", "開盤", "最低", "最高", "收盤", "還原", "成交量"]
)
#-----設定treeview欄位-----#
#tree.bind("<<TreeviewSelect>>", item_select)
tree.heading(0, text="日期")
tree.heading(1, text="開盤")
tree.heading(2, text="最低")
tree.heading(3, text="最高")
tree.heading(4, text="收盤")
tree.heading(5, text="還原")
tree.heading(6, text="成交量")
#-----設定treeview格式-----#
tree.column(0, anchor="center", width=130)
tree.column(1, anchor="center", width=130)
tree.column(2, anchor="center", width=130)
tree.column(3, anchor="center", width=130)
tree.column(4, anchor="center", width=130)
tree.column(5, anchor="center", width=130)
tree.column(6, anchor="center", width=130)
tree.pack()


#-----設定線圖框-----#
line=tk.Button(fifthFrame,text='顯示移動平均線圖',command=pop_up).pack()


#-----當按下右上角關閉視窗時，停止執行py檔案-----#
Window.protocol("WM_DELETE_WINDOW", Window.quit)


#-----保持視窗在執行狀態-----#
Window.mainloop()