import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import pandas as pd
from tkinter import Tk, Label
from PIL import Image, ImageTk  # 載入PIL庫
import csv,os
from tkinter import filedialog, ttk
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt  # 引入 matplotlib

class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # ======= 基本設置 =======
        self.title("風扇貼標正確判斷")
        style = ttk.Style(self)
        style.configure("Topframe.Tabel", font=("Helvetica", 20))  # 標題樣式
        font1 = ("標楷體", 12)

        # ======= 讀取數據 =======
        self.df = pd.read_csv('Factoryworkstation.csv')  # 調整為你的檔案路徑
        self.data = pd.read_csv('virtual_data_with_permissions.csv')##
        self.frame0_data = pd.read_csv('orders_large.csv')

        # ======= 標題部分 =======
        topFrame = ttk.Frame(self)
        ttk.Label(topFrame, text="風扇貼標歪斜檢測", font=("Helvetica", 40)).pack(padx=20, pady=20)
        topFrame.pack()

        # ======= 中間選項部分 =======
        midFrame = ttk.Frame(self)
        frame0 = ttk.Frame(midFrame)

        # ================= date  =====================
        tk.Label(frame0, text="日期:", font=font1).pack(side="left", padx=5, pady=5)
        self.date_county = tk.StringVar()
        self.date_cobox = ttk.Combobox(frame0, textvariable=self.date_county,values=self.get_date_values('Date'),state="readonly",width=10)
        self.date_cobox.set("請選擇日期")
        self.date_cobox.pack(side="left", padx=5)
        self.date_cobox.bind("<<ComboboxSelected>>", self.update_OrderID_options)
        # ================= date  =====================
        date=self.date_county.get()
        print(date)
        # ================= OrderID  =====================
        tk.Label(frame0, text="訂單號碼:", font=font1).pack(side="left", padx=5, pady=5)
        self.OrderID_county = tk.StringVar()
        self.OrderID_cobox = ttk.Combobox(frame0, textvariable=self.OrderID_county,state="readonly",width=10)
        self.OrderID_cobox.set("訂單號碼")
        self.OrderID_cobox.pack(side="left", padx=5)
        self.OrderID_cobox.bind("<<ComboboxSelected>>", self.update_Product_Quantity)  # 更新Product和Quantity選項
        # ================= OrderID  =====================
        # ================= Product  =====================
        tk.Label(frame0, text="訂單料號:", font=font1).pack(side="left", padx=5, pady=5)
        self.Product_county = tk.StringVar()
        self.Product_cobox = ttk.Combobox(
            frame0, textvariable=self.Product_county,state="readonly",width=15)
        self.Product_cobox.set("訂單料號")
        self.Product_cobox.pack(side="left", padx=5)
        # ================= Product  =====================
        # ================= Quantity  =====================        
        tk.Label(frame0, text="訂單數量:", font=font1).pack(side="left", padx=5, pady=5)
        self.Quantity_county = tk.StringVar()
        self.Quantity_cobox = ttk.Combobox(frame0, textvariable=self.Quantity_county,state="readonly",width=8)
        self.Quantity_cobox.set("訂單數量")
        self.Quantity_cobox.pack(side="left", padx=5)
        frame0.pack()
        # ================= Quantity  =====================
        # ================= Factory  =====================
        tk.Label(frame0, text="廠區:", font=font1).pack(side="left", padx=5, pady=5)
        self.Factory_county = tk.StringVar()
        self.Factory_cobox = ttk.Combobox(frame0, textvariable=self.Factory_county,values=self.get_unique_values('Plant'),state="readonly",width=10)
        self.Factory_cobox.set("請選擇廠區")
        self.Factory_cobox.pack(side="left", padx=5)
        self.Factory_cobox.bind("<<ComboboxSelected>>", self.update_workshop_options)
        # ================= Factory  =====================
        # ================= workshop  ====================
        tk.Label(frame0, text="車間:", font=font1).pack(side="left", padx=5, pady=5)
        self.workshop_county = tk.StringVar()
        self.workshop_cobox = ttk.Combobox(frame0, textvariable=self.workshop_county,state="readonly",width=10)
        self.workshop_cobox.set("請選擇車間")
        self.workshop_cobox.pack(side="left", padx=5)
        self.workshop_cobox.bind("<<ComboboxSelected>>", self.update_code_options)
        # ================= workshop  ====================
        # ================= workstation===================
        tk.Label(frame0, text="工站:", font=font1).pack(side="left", padx=5, pady=5)
        self.workstation_county = tk.StringVar()
        self.workstation_cobox = ttk.Combobox(frame0, textvariable=self.workstation_county,state="readonly",width=10)
        self.workstation_cobox.set("請選擇工站")
        self.workstation_cobox.pack(side="left", padx=5)
        # ================= workstation===================
        #=====================製造ID========================================================
        frame2 = ttk.Frame(midFrame)
        tk.Label(frame2, text="製造者ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.manufacturer_id = tk.StringVar()
        self.manufacturer_cobox = ttk.Combobox(frame2, textvariable=self.manufacturer_id,state="readonly",width=15)
        self.manufacturer_cobox.set("請選擇製造者ID")
        self.manufacturer_cobox.bind("<<ComboboxSelected>>", self.update_manufacturer_name)
        self.manufacturer_cobox.pack(side="left", padx=5)
        self.update_manufacturer_options() 
        tk.Label(frame2, text="製造者:", font=font1).pack(side="left", padx=5, pady=5)
        self.manufacturer_name_id = tk.StringVar()  
        self.manufacturer_name_cobox = ttk.Combobox(frame2, textvariable=self.manufacturer_name_id,state="readonly",width=15)
        self.manufacturer_name_cobox.set("請選擇製造者ID") 
        self.manufacturer_name_cobox.pack(side="left", padx=5)
        #=====================製造ID========================================================
        #=====================品保ID========================================================
        tk.Label(frame2, text="品保ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.quality_control_id = tk.StringVar()
        self.quality_control_cobox = ttk.Combobox(frame2, textvariable=self.quality_control_id,state="readonly",width=15)        
        self.quality_control_cobox.set("請選擇品保ID")
        self.quality_control_cobox.bind("<<ComboboxSelected>>", self.update_quality_control_name)
        self.quality_control_cobox.pack(side="left", padx=5)
        self.update_quality_control_options()
        tk.Label(frame2, text="品保:", font=font1).pack(side="left", padx=5, pady=5)
        self.quality_name_id = tk.StringVar()
        self.quality_name_cobox = ttk.Combobox(frame2, textvariable=self.quality_name_id,state="readonly",width=15)
        self.quality_name_cobox.set("請選擇品保ID")
        self.quality_name_cobox.pack(side="left", padx=5)
        #=====================品保ID========================================================
        #=====================組長ID========================================================
        tk.Label(frame2, text="組長ID:", font=font1).pack(side="left", padx=5, pady=5)
        self.team_leader_id = tk.StringVar()
        self.team_leader_cobox = ttk.Combobox(frame2, textvariable=self.team_leader_id,state="readonly",width=15)
        self.team_leader_cobox.set("請選擇組長ID")
        self.team_leader_cobox.bind("<<ComboboxSelected>>", self.update_team_leader_name)
        self.team_leader_cobox.pack(side="left", padx=5)
        self.update_team_leader_options()
        tk.Label(frame2, text="組長:", font=font1).pack(side="left", padx=5, pady=5)
        self.team_name_id = tk.StringVar()
        self.team_name_cobox = ttk.Combobox(frame2, textvariable=self.team_name_id,state="readonly",width=15)
        self.team_name_cobox.set("請選擇組長ID")
        self.team_name_cobox.pack(side="left", padx=5)    
        #=====================組長ID========================================================
 
        frame2.pack(pady=10)

        midFrame.pack(pady=20)
        # ================= 讀取圖片 =============================================================================
         # ======= 初始化變數 =======
        self.image_folder = None
        self.image_files = []
        self.image_index = 0
        self.current_csv_path = None  # 當前處理的 CSV 檔案
        self.image_id = 1  # 流水號初始值

        # 置信度與預測結果資料
        self.confidences = []
        self.predictions = []

        # 載入模型
        self.model = load_model('resnet50_5_model.h5')

        # ======= 左邊圖片顯示區 =======
        
        # ======= 左邊圖片顯示區 =======
        # 新增左側框架
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left", padx=20, pady=20)

        # 上方的文字與按鈕框架
        self.top_button_frame = tk.Frame(self.left_frame)
        self.top_button_frame.pack(side="top", fill="x", pady=10)

        # 顯示提示文字
        self.label = Label(self.top_button_frame, text="請選擇圖片資料夾", font=("Arial", 16))
        self.label.pack(side="left", padx=5)

        # 按鈕：選擇圖片資料夾
        self.folder_button = tk.Button(self.top_button_frame, text="選擇圖片資料夾", command=self.select_folder)
        self.folder_button.pack(side="left", padx=5)

        # 按鈕：生成預測圖表
        self.chart_button = tk.Button(self.top_button_frame, text="生成預測圖表", command=self.plot_chart)
        self.chart_button.pack(side="left", padx=5)

        # 顯示圖片的區域
        self.image_label = Label(self.left_frame)  # 顯示圖片的區域
        self.image_label.pack(padx=20, pady=20)


  

        # ======= 右邊 TreeView =======
        self.tree_frame = ttk.Frame(self)
        self.tree_label = Label(self.tree_frame, text="CSV 檔案內容", font=("Arial", 14))
        self.tree = ttk.Treeview(self.tree_frame, show="headings", height=20)

        # 初始隱藏 TreeView
        self.tree_hidden = True
        self.hide_tree()


    def hide_tree(self):
        """隱藏 TreeView 和標籤"""
        self.tree_label.pack_forget()
        self.tree.pack_forget()
        self.tree_frame.pack_forget()
        self.tree_hidden = True

    def show_tree(self):
        """顯示 TreeView 和標籤"""
        self.tree_frame.pack(side="right", fill="both", expand=True, padx=10)
        self.tree_label.pack(pady=10)
        self.tree.pack(fill="both", expand=True)
        self.tree_hidden = False

    def refresh_csv_content(self):
        """刷新 TreeView 內容，並根據資料決定是否顯示 TreeView"""
        if not self.current_csv_path or not os.path.exists(self.current_csv_path):
            return

        # 清空現有的 TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 讀取 CSV 並更新 TreeView
        with open(self.current_csv_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) > 1:  # 如果有資料（不包括標頭）
                # 顯示 TreeView
                if self.tree_hidden:
                    self.show_tree()

                # 更新 TreeView 標頭
                self.tree["columns"] = rows[0]
                for column in rows[0]:
                    self.tree.heading(column, text=column)
                    self.tree.column(column, width=100, anchor="w")

                # 插入行
                for i, row in enumerate(rows[1:], start=1):  # 從第二行開始
                    self.tree.insert("", "end", values=row)
            else:
                # 如果資料僅有表頭，隱藏 TreeView
                self.hide_tree()

    def select_folder(self):
        """選擇圖片資料夾"""
        self.image_folder = filedialog.askdirectory(title="選擇圖片資料夾")
        if self.image_folder:
            self.image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.image_index = 0
            self.load_image()
            self.auto_process_images()  # 開始自動處理圖片

    def load_image(self):
        """載入當前圖片"""
        if self.image_files and 0 <= self.image_index < len(self.image_files):
            img_path = os.path.join(self.image_folder, self.image_files[self.image_index])
            img = Image.open(img_path).resize((400, 400))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def change_image_and_write_csv(self):
        """切換圖片並寫入 CSV"""
        if not self.image_files:
            return

        # ======= 收集數據 =======
        img_path = os.path.join(self.image_folder, self.image_files[self.image_index])
        date = self.date_county.get()
        OrderID = self.OrderID_county.get()
        Product = self.Product_county.get()
        Quantity = self.Quantity_county.get()
        Factory = self.Factory_county.get()
        workstation = self.workstation_county.get()
        manufacturer_id = self.manufacturer_id.get()
        manufacturer_name_id = self.manufacturer_name_id.get()
        quality_control_id = self.quality_control_id.get()
        quality_name_id = self.quality_name_id.get()
        team_leader_id = self.team_leader_id.get()
        team_name_id = self.team_name_id.get()

        # 確保當前 CSV 檔案
        self.current_csv_path = os.path.join(self.image_folder, f"{OrderID}_{date}.csv")

        # 載入圖片並進行預測
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # 增加批次維度
        img_array = img_array / 255.0  # 進行歸一化

        # 預測
        prediction = self.model.predict(img_array)[0][0]  # 獲得預測值
        confidence = float(prediction)  # 置信度是預測值
        final_label = int(round(confidence))  # 0 或 1 的預測結果

        # 更新置信度和預測結果
        self.confidences.append(confidence)
        self.predictions.append(final_label)

        # 寫入 CSV
        with open(self.current_csv_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            if os.stat(self.current_csv_path).st_size == 0:  # 檢查檔案是否為空，如果是，寫入表頭
                writer.writerow(['ID', 'Date', 'OrderID', 'Product', 'Quantity', 'Factory', 'Workstation', 'ManufacturerID',
                                 'ManufacturerNameID', 'QualityControlID', 'QualityNameID', 'TeamLeaderID', 'TeamNameID',
                                 'ImagePath', 'Prediction', 'Confidence'])

            # 寫入資料
            writer.writerow([self.image_id, date, OrderID, Product, Quantity, Factory, workstation, manufacturer_id,
                             manufacturer_name_id, quality_control_id, quality_name_id, team_leader_id, team_name_id,
                             img_path, final_label, confidence])

        # 更新圖片清單，移除已處理的圖片
        self.image_files.pop(self.image_index)

        # 增加流水號
        self.image_id += 1

        # 刷新 TreeView
        self.refresh_csv_content()

        # 如果還有圖片，繼續處理
        if self.image_files:
            self.image_index = self.image_index % len(self.image_files)  # 確保圖片索引在範圍內
            self.load_image()  # 顯示下一張圖片
        else:
            self.label.config(text="所有圖片處理完成！")

    def plot_chart(self):
        """生成預測結果與置信度圖表"""
        if not self.confidences or not self.predictions:
            return

        # 創建圖表
        plt.figure(figsize=(10, 6))

        # 繪製置信度與預測結果
        plt.subplot(1, 2, 1)
        plt.plot(self.confidences, label="Confidence", color="blue")
        plt.xlabel("Image Index")
        plt.ylabel("Confidence")
        plt.title("Confidence Over Images")
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.predictions, label="Prediction", color="green")
        plt.xlabel("Image Index")
        plt.ylabel("Prediction")
        plt.title("Prediction Over Images")
        plt.legend()

        # 顯示圖表
        plt.tight_layout()
        plt.show()

    def auto_process_images(self):
        """自動處理圖片並寫入 CSV"""
        if not self.image_files:
            return

        # 每處理完一張圖片，休眠一段時間後自動切換
        self.after(2000, self.process_next_image)  # 每兩秒處理一次圖片

    def process_next_image(self):
        """處理下一張圖片"""
        self.change_image_and_write_csv()  # 寫入資料
        if self.image_files:
            self.auto_process_images()  # 繼續處理下一張圖片



     # ================= 讀取圖片 =============================================================================
    # ======= 工具方法 =======
    def get_date_values(self, name):
        return self.frame0_data[name].dropna().unique().tolist()

    def update_OrderID_options(self, event):
        selected_date = self.date_county.get()
        if selected_date:
            filtered_OrderID = self.frame0_data[self.frame0_data['Date'] == selected_date]['OrderID'].unique().tolist()
            self.OrderID_cobox['values'] = filtered_OrderID

    def update_Product_Quantity(self, event):
        selected_date = self.date_county.get()  # 取得選擇的日期
        selected_order_id = self.OrderID_county.get()  # 取得選擇的訂單號碼
        
        if selected_date and selected_order_id:
            # 根據 Date 和 OrderID 篩選符合條件的 Product 和 Quantity
            filtered_data = self.frame0_data[
                (self.frame0_data['Date'] == selected_date) & 
                (self.frame0_data['OrderID'] == selected_order_id)
            ]
            
            # 更新訂單料號 (Product) 和 訂單數量 (Quantity) 選項
            products = filtered_data['Product'].unique().tolist()
            quantities = filtered_data['Quantity'].unique().tolist()

            self.Product_cobox['values'] = products
            self.Quantity_cobox['values'] = quantities

            if products:
                self.Product_cobox.set(products[0])  # 預設選擇第一個產品料號
            if quantities:
                self.Quantity_cobox.set(quantities[0])  # 預設選擇第一個訂單數量

    def get_unique_values(self, column_name):
        return self.df[column_name].dropna().unique().tolist()

    def update_workshop_options(self, event):
        selected_plant = self.Factory_county.get()
        if selected_plant:
            filtered_workstations = self.df[self.df['Plant'] == selected_plant]['Workstation Code'].unique().tolist()
            self.workshop_cobox['values'] = filtered_workstations
            self.workshop_cobox.set("請選擇車間")
            self.workstation_cobox.set("請選擇工站")
            self.workstation_cobox['values'] = []

    def update_code_options(self, event):
        selected_plant = self.Factory_county.get()
        selected_workstation = self.workshop_county.get()
        if selected_plant and selected_workstation:
            filtered_codes = self.df[
                (self.df['Plant'] == selected_plant) & 
                (self.df['Workstation Code'] == selected_workstation)
            ]['Code'].unique().tolist()
            self.workstation_cobox['values'] = filtered_codes
            self.workstation_cobox.set("請選擇工站")
    def update_manufacturer_options(self):# 假設此方法會更新製造者ID選項
        manufacturer_ids = self.data[self.data['權限代號'] == 1]['ID'].unique().tolist()# 更新製造者ID選項
        self.manufacturer_cobox['values'] = manufacturer_ids# 預設顯示文字
        self.manufacturer_cobox.set("請選擇製造者ID")
    def update_quality_control_options(self):# 假設此方法會更新品保ID選項
        quality_control_ids = self.data[self.data['權限代號'] == 3]['ID'].unique().tolist()# 更新品保ID選項
        self.quality_control_cobox['values'] = quality_control_ids# 預設顯示文字
        self.quality_control_cobox.set("請選擇品保ID")
    def update_team_leader_options(self):# 假設此方法會更新組長ID選項
        team_leader_ids = self.data[self.data['權限代號'] == 2]['ID'].unique().tolist()# 更新組長ID選項
        self.team_leader_cobox['values'] = team_leader_ids# 預設顯示文字
        self.team_leader_cobox.set("請選擇組長ID")
    def update_manufacturer_name(self, event):
        selected_id = self.manufacturer_id.get()  # 取得選擇的製造者 ID
        if selected_id:# 根據選擇的 ID 查詢對應的姓名
            filtered_name = self.data[self.data['ID'] == selected_id]['姓名'].tolist()
            if filtered_name:
                self.manufacturer_name_cobox.set(filtered_name[0])  # 設定對應的姓名
            else:
                self.manufacturer_name_cobox.set("未找到對應姓名")
    def update_quality_control_name(self, event):
        selected_id = self.quality_control_id.get()  # 取得選擇的品保 ID
        if selected_id:# 根據選擇的 ID 查詢對應的姓名
            filtered_name = self.data[self.data['ID'] == selected_id]['姓名'].tolist()
            if filtered_name:
                self.quality_name_cobox.set(filtered_name[0])  # 設定對應的姓名
            else:
                self.quality_name_cobox.set("未找到對應姓名")
    def update_team_leader_name(self, event):
        selected_id = self.team_leader_id.get()  # 取得選擇的組長 ID
        if selected_id:# 根據選擇的 ID 查詢對應的姓名
            filtered_name = self.data[self.data['ID'] == selected_id]['姓名'].tolist()
            if filtered_name:
                self.team_name_cobox.set(filtered_name[0])  # 設定對應的姓名
            else:
                self.team_name_cobox.set("未找到對應姓名")


if __name__ == "__main__":
    window = Window()
    window.mainloop()