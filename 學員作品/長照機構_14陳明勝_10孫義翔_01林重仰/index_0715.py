import json
import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView

# 載入 JSON 檔案
with open('/Users/danny/Documents/TVDI_Project_LTC/Data/長照機構總表_雙北市.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 區域代碼對應表
area_mapping = {
    63000010: "松山區",
    63000020: "信義區",
    63000030: "大安區",
    63000040: "中山區",
    63000050: "中正區",
    63000060: "大同區",
    63000070: "萬華區",
    63000080: "文山區",
    63000090: "南港區",
    63000100: "內湖區",
    63000110: "士林區",
    63000120: "北投區",
    65000010: "板橋區",
    65000020: "三重區",
    65000030: "中和區",
    65000040: "永和區",
    65000050: "新莊區",
    65000060: "新店區",
    65000070: "樹林區",
    65000080: "鶯歌區",
    65000090: "三峽區",
    65000100: "淡水區",
    65000110: "汐止區",
    65000120: "瑞芳區",
    65000130: "土城區",
    65000140: "蘆洲區",
    65000150: "五股區",
    65000160: "泰山區",
    65000170: "林口區",
    65000180: "深坑區",
    65000190: "石碇區",
    65000200: "坪林區",
    65000210: "三芝區",
    65000220: "石門區",
    65000230: "八里區",
    65000240: "平溪區",
    65000250: "雙溪區",
    65000260: "貢寮區",
    65000270: "金山區",
    65000280: "萬里區",
    65000290: "烏來區"
}

# 分離台北市和新北市的資料
taipei_data = [entry for entry in data if entry['縣市'] == 63000]
new_taipei_data = [entry for entry in data if entry['縣市'] == 65000]

# 建立主視窗
root = tk.Tk()
root.title("長照機構資訊")
root.geometry("1200x800")

# 設置背景顏色
style = ttk.Style()
root.configure(background='lightblue')
style.configure('TFrame', background='lightblue')
style.configure('TLabel', background='lightblue', font=("Microsoft JhengHei", 12))
style.configure('TCombobox', fieldbackground='lightblue', background='lightblue', font=("Microsoft JhengHei", 12))
style.configure('Treeview', font=("Microsoft JhengHei", 12))
style.configure('Treeview.Heading', font=("Microsoft JhengHei", 14, 'bold'))

# 用於存儲各區域的資料
self_areas = {
    "台北市": {v: [] for k, v in area_mapping.items() if k // 1000 == 63000},
    "新北市": {v: [] for k, v in area_mapping.items() if k // 1000 == 65000}
}

# 將資料根據區域分配到 self_areas
for item in taipei_data:
    area_name = area_mapping.get(item['區'])
    if area_name:
        self_areas["台北市"][area_name].append(item)

for item in new_taipei_data:
    area_name = area_mapping.get(item['區'])
    if area_name:
        self_areas["新北市"][area_name].append(item)

def update_treeview(city, area):
    for i in tree.get_children():
        tree.delete(i)
    for item in self_areas[city][area]:
        tree.insert('', 'end', values=(item['機構名稱'], item['地址全址'], item['機構電話'], item['特約服務項目']))

def on_city_change(event):
    city = city_var.get()
    if city == "請選擇城市":
        area_menu['values'] = ["請選擇行政區"]
        area_menu.current(0)
        return
    area_menu['values'] = list(self_areas[city].keys())
    area_menu.current(0)
    update_treeview(city, area_menu.get())

def on_area_change(event):
    if area_menu.get() != "請選擇行政區":
        update_treeview(city_var.get(), area_menu.get())

city_var = tk.StringVar(value="請選擇城市")
city_menu = ttk.Combobox(root, textvariable=city_var, values=["請選擇城市", "台北市", "新北市"])
city_menu.bind("<<ComboboxSelected>>", on_city_change)
city_menu.pack(pady=10)

# 建立區域選單
area_var = tk.StringVar(value="請選擇行政區")
area_menu = ttk.Combobox(root, textvariable=area_var, values=["請選擇行政區"])
area_menu.bind("<<ComboboxSelected>>", on_area_change)
area_menu.pack(pady=10)

# 建立 Treeview 來顯示資料
frame = ttk.Frame(root)
frame.pack(expand=True, fill='both')

columns = ("名稱", "地址", "電話", "特約服務項目")
tree = ttk.Treeview(frame, columns=columns, show='headings')
tree.heading("名稱", text="名稱", anchor="center")
tree.heading("地址", text="地址", anchor="center")
tree.heading("電話", text="電話", anchor="center")
tree.heading("特約服務項目", text="特約服務項目", anchor="center")

for col in columns:
    tree.column(col, anchor="center")

tree.pack(side='left', expand=True, fill='both')

# 增加滾動條
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# 初始載入空白的資料
area_menu['values'] = ["請選擇行政區"]
area_menu.current(0)

# 建立地圖顯示功能
def show_on_map(event):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, 'values')
    address = values[1]
    for item in taipei_data + new_taipei_data:
        if item['地址全址'] == address:
            latitude = item['緯度']
            longitude = item['經度']
            break
    map_view = tk.Toplevel(root)
    map_view.title("地圖")
    map_widget = TkinterMapView(map_view, width=800, height=600)
    map_widget.pack(expand=True, fill='both')
    map_widget.set_position(latitude, longitude)
    map_widget.set_marker(latitude, longitude, text=values[0])

tree.bind("<Double-1>", show_on_map)

root.mainloop()
