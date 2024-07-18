import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os

# 讀取CSV資料
file_path = os.path.join('annual_averages.csv')
annual_averages_df = pd.read_csv(file_path)

# 定義太陽能系統相關常數
WATT_PER_PANEL = 400  # 每塊太陽能板的瓦數
PANEL_PRICE_RANGE = (250, 360)  # 每塊太陽能板的價格區間（美元）
USD_TO_TWD = 30  # 美元兌新台幣匯率
DAILY_ENERGY_THRESHOLD = 11  # 每日能量需求閾值（度）
SYSTEM_EFFICIENCY = 0.8  # 太陽能系統效率
AREA_PER_PANEL = 1.7  # 每塊太陽能板所需的面積（平方公尺）

# 其他設備價格範圍（美元）
ROOF_MOUNT_PRICE_RANGE = (1000, 3000)
GROUND_MOUNT_PRICE_RANGE = (2000, 4000)
STRING_INVERTER_PRICE_RANGE = (1000, 2500)
MICROINVERTER_PRICE_RANGE = (3000, 5000)
BATTERY_PRICE_RANGE = (4000, 7000)  # 鋰離子電池
CHARGE_CONTROLLER_PRICE_RANGE = (100, 500)
DISCONNECT_SWITCH_PRICE_RANGE = (50, 200)
LABOR_COST_RANGE = (3000, 7000)

# 定義根據樓地板面積計算每日預估發電量的函數
def calculate_daily_energy(floor_area_tsubo, esh):
    floor_area_m2 = floor_area_tsubo * 3.305785
    num_panels = floor_area_m2 / AREA_PER_PANEL
    total_watt = num_panels * WATT_PER_PANEL
    daily_energy = total_watt * esh * SYSTEM_EFFICIENCY / 1000  # 轉換成度
    return daily_energy

# 定義根據樓地板面積預估安裝價格的函數
def estimate_installation_cost(floor_area_tsubo, roof_mount=True):
    floor_area_m2 = floor_area_tsubo * 3.305785
    num_panels = floor_area_m2 / AREA_PER_PANEL
    panel_cost = num_panels * (sum(PANEL_PRICE_RANGE) / 2)
    
    mount_cost = sum(ROOF_MOUNT_PRICE_RANGE) / 2 if roof_mount else sum(GROUND_MOUNT_PRICE_RANGE) / 2
    inverter_cost = sum(STRING_INVERTER_PRICE_RANGE) / 2
    battery_cost = sum(BATTERY_PRICE_RANGE) / 2
    controller_cost = sum(CHARGE_CONTROLLER_PRICE_RANGE) / 2
    switch_cost = sum(DISCONNECT_SWITCH_PRICE_RANGE) / 2
    labor_cost = sum(LABOR_COST_RANGE) / 2
    
    total_cost_usd = panel_cost + mount_cost + inverter_cost + battery_cost + controller_cost + switch_cost + labor_cost
    total_cost_twd = total_cost_usd * USD_TO_TWD
    
    return total_cost_twd

# 定義建議是否安裝的函數
def suggest_installation(floor_area_tsubo, esh, roof_mount=True):
    daily_energy = calculate_daily_energy(floor_area_tsubo, esh)
    installation_cost = estimate_installation_cost(floor_area_tsubo, roof_mount)
    suggestion = "建議安裝" if daily_energy > DAILY_ENERGY_THRESHOLD else "不建議安裝"
    return suggestion, daily_energy, installation_cost

# 定義處理按鈕點擊的函數
def on_submit(region_var, floor_area_var, result_var):
    region = region_var.get()
    try:
        floor_area_tsubo = float(floor_area_var.get())
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的樓地板面積")
        return
    
    esh = annual_averages_df[annual_averages_df['行政區'] == region]['ESH'].mean()
    
    if esh is None or pd.isna(esh):
        messagebox.showerror("資料錯誤", "無法找到該區域的ESH資料")
        return
    
    suggestion, daily_energy, installation_cost = suggest_installation(floor_area_tsubo, esh)
    
    result_var.set(f"{suggestion}\n每日預估發電量: {daily_energy:.2f} 度\n預估安裝成本: {installation_cost:.2f} 新台幣")

# GUI 應用設定
def create_ui(window):
    # 建立視窗部件
    ttk.Label(window, text="選擇區域:").grid(column=0, row=0, padx=10, pady=10)
    region_var = tk.StringVar()
    region_combo = ttk.Combobox(window, textvariable=region_var)
    region_combo['values'] = annual_averages_df['行政區'].unique().tolist()
    region_combo.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(window, text="樓地板面積 (坪):").grid(column=0, row=1, padx=10, pady=10)
    floor_area_var = tk.StringVar()
    ttk.Entry(window, textvariable=floor_area_var).grid(column=1, row=1, padx=10, pady=10)

    result_var = tk.StringVar()
    ttk.Label(window, textvariable=result_var).grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    ttk.Button(window, text="提交", command=lambda: on_submit(region_var, floor_area_var, result_var)).grid(column=0, row=2, columnspan=2, padx=10, pady=10)

