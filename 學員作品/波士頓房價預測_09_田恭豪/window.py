import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, Button
from dataset import getInfo
import numpy as np       #數學處理
import pandas as pd       #資料處理
import matplotlib.pyplot as plt #繪圖
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import analysis


# 使用 getInfo 函數從 dataset.py 中載入資料集
df = getInfo()

# 如果資料集為空，處理異常情況
if df.empty:
    print("無法載入資料集，請檢查文件路徑。")
    exit()

# =================================================

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font', ('Tahoma', 15, 'bold'))
        self.title("波士頓房價預測")
        self.geometry("800x620")
        
        # 呼叫函數以居中視窗
        self.center_window(800, 620)

        self.create_widgets()

        # 初始化 Treeview 相關變量
        self.tree_frame1 = None
        self.tree1 = None
        self.tree_frame2 = None
        self.tree2 = None

        # 設置窗口關閉時的處理
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # 創建框架放置標籤和按鈕
        self.frame = tk.Frame(self)
        self.frame.pack(anchor="nw", padx=5, pady=5)

        # 標籤設計
        self.label = tk.Label(self.frame, text="波士頓房價", bg="lightblue", relief="raised", padx=20, pady=10)
        self.label.pack(side="left")

        # combobox設計
        self.combobox = ttk.Combobox(self.frame, values=["數據一", "數據二", "數據三"], state="readonly")
        self.combobox.set("請選擇圖表:")
        self.combobox.pack(side="left", padx=(5, 0))

        # 按鈕設計，包括文字和向下箭頭圖案
        self.show_btn = tk.Button(self.frame, text="查看資料 \u21E9", pady=5, font=('Tahoma', 12,'bold'), command=self.show_data, relief="raised", borderwidth=5)
        self.show_btn.pack(side="left", padx=(5, 0))

        # 恢復初始狀態按鈕
        self.reset_btn = tk.Button(self.frame, text="恢復初始狀態", pady=5, font=('Tahoma', 12,'bold'), command=self.reset_data, relief="raised", borderwidth=5)
        self.reset_btn.pack(side="left", padx=(5, 10))

        # 新增按鈕 "評分"
        self.open_options_btn = tk.Button(self.frame, text="評分", pady=5, font=('Tahoma', 12,'bold'), command=self.show_rating_dialog, relief="raised", borderwidth=5)
        self.open_options_btn.pack(side="left")

        # 添加背景框架，並填充視窗下方
        self.background_frame = tk.Frame(self, bg="#FBF6E2")
        self.background_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def center_window(self, width=800, height=600):
        # 取得螢幕的寬度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 計算視窗的位置，使其位於螢幕中央
        position_x = (screen_width - width) // 2
        position_y = (screen_height - height) // 2

        # 設定視窗的寬度、高度及位置
        self.geometry(f'{width}x{height}+{position_x}+{position_y}')

    def show_data(self):
        selected_option = self.combobox.get()
        if selected_option == "請選擇圖表:":
            messagebox.showwarning("警告", "請先選擇一個選項")
            return
        
        if selected_option == "數據一":
            if self.tree1 is None:
                self.create_treeview1()
            if self.tree2 is None:
                self.create_treeview2()
        elif selected_option == "數據二":
            self.show_data_window()
        elif selected_option == "數據三":
            self.show_additional_data_window()

    def create_treeview1(self):
        self.destroy_treeview1()

        self.tree_frame1 = tk.Frame(self.background_frame)
        self.tree_frame1.pack(pady=10, padx=(10, 370))

        # 新增treeview標籤1
        self.label1 = tk.Label(self.tree_frame1, text="資料集", padx=20)
        self.label1.pack(side="top")

        self.tree1 = ttk.Treeview(self.tree_frame1, columns=("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"), show="headings")

        for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"):
            self.tree1.heading(col, text=col, anchor="center")
            self.tree1.column(col, anchor="center", width=80, stretch=False)

        vsb1 = ttk.Scrollbar(self.tree_frame1, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=vsb1.set)
        vsb1.pack(side="right", fill="y")

        hsb1 = ttk.Scrollbar(self.tree_frame1, orient="horizontal", command=self.tree1.xview)
        self.tree1.configure(xscrollcommand=hsb1.set)
        hsb1.pack(side="bottom", fill="x")

        self.tree1.pack(side="left", fill="both", expand=True)
        self.tree_frame1.grid_rowconfigure(0, weight=1)
        self.tree_frame1.grid_columnconfigure(0, weight=1)

        try:
            df = pd.read_csv("train_dataset.csv")
            for index, row in df.head(20).iterrows():
                data = tuple(row)
                self.tree1.insert("", "end", values=data)
        except FileNotFoundError:
            print("找不到指定的 CSV 檔案。")

    def create_treeview2(self):
        self.destroy_treeview2()

        self.tree_frame2 = tk.Frame(self.background_frame)
        self.tree_frame2.pack(pady=10, padx=(10, 370), fill="both", expand=True)

        # 新增treeview標籤2
        self.label2 = tk.Label(self.tree_frame2, text="敘述統計", padx=20)
        self.label2.pack(side="top")

        self.tree2 = ttk.Treeview(self.tree_frame2, columns=("Statistic", "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"), show="headings")

        # 設置標題
        self.tree2.heading("Statistic", text="Statistic", anchor="center")
        self.tree2.column("Statistic", width=60, stretch=False)

        for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE"):
            self.tree2.heading(col, text=col, anchor="center")
            self.tree2.column(col, width=80, stretch=False)

        hsb2 = ttk.Scrollbar(self.tree_frame2, orient="horizontal", command=self.tree2.xview)
        self.tree2.configure(xscrollcommand=hsb2.set)
        hsb2.pack(side="bottom", fill="x")

        self.tree2.pack(side="left", fill="both", expand=True)
        self.tree_frame2.grid_rowconfigure(0, weight=1)
        self.tree_frame2.grid_columnconfigure(0, weight=1)

        try:
            df = pd.read_csv("train_dataset.csv")
            stats = df.describe()

            for stat_index, stat_name in enumerate(["count", "mean", "std", "min", "25%", "50%", "75%", "max"]):
                values = [stat_name] + [stats.loc[stat_name, col] for col in ("CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO", "B", "LSTAT", "PRICE")]
                self.tree2.insert("", "end", values=values)
        except FileNotFoundError:
            print("找不到指定的 CSV 檔案")

    def reset_data(self):
        self.destroy_treeview1()
        self.destroy_treeview2()

        # 將 combobox 設置為初始值 "請選擇圖表"
        self.combobox.set("請選擇圖表:")

    def destroy_treeview1(self):
        if self.tree_frame1 is not None:
            self.tree_frame1.destroy()
            self.tree_frame1 = None
            self.tree1 = None

    def destroy_treeview2(self):
        if self.tree_frame2 is not None:
            self.tree_frame2.destroy()
            self.tree_frame2 = None
            self.tree2 = None

    def show_data_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("數據二")
        new_window.geometry("650x450")

        try:
            # 圖表描述標籤
            chart_label = tk.Label(new_window, text="缺失值處理 與 合鬚圖", font=('Tahoma', 15, 'bold'))
            chart_label.pack(side=tk.TOP, pady=5)    

            # 圖片1
            image_path1 = r"C:\Users\user\Documents\GitHub\__11304_python_2024_tvdi__\homework\專案\波士頓房價預測_09_田恭豪\images\image_1.png"
            image1 = Image.open(image_path1)
            image1 = image1.resize((250, 400), Image.LANCZOS)
            photo1 = ImageTk.PhotoImage(image1)

            label1 = tk.Label(new_window, image=photo1)
            label1.image = photo1  # 保持對圖像的引用
            label1.pack(side=tk.LEFT, padx=(10,5), pady=5)

            # 圖片2
            image_path2 = r"C:\Users\user\Documents\GitHub\__11304_python_2024_tvdi__\homework\專案\波士頓房價預測_09_田恭豪\images\image_2.png"
            image2 = Image.open(image_path2)
            image2 = image2.resize((350, 400), Image.LANCZOS)
            photo2 = ImageTk.PhotoImage(image2)

            label2 = tk.Label(new_window, image=photo2)
            label2.image = photo2  # 保持對圖像的引用
            label2.pack(side=tk.LEFT, padx=(5,10), pady=5)
        except FileNotFoundError as e:
            messagebox.showerror("錯誤", f"找不到指定的圖片檔案：{e}")

    def show_additional_data_window(self):
        new_window = tk.Toplevel(self)
        new_window.title("數據三")
        new_window.geometry("850x420")

        try:
            # 圖表描述標籤
            chart_label = tk.Label(new_window, text="常態分佈圖 與 熱力圖", font=('Tahoma', 15, 'bold'))
            chart_label.pack(side=tk.TOP, pady=5)

            # 圖片3
            image_path3 = r"C:\Users\user\Documents\GitHub\__11304_python_2024_tvdi__\homework\專案\波士頓房價預測_09_田恭豪\images\image_3.png"
            image3 = Image.open(image_path3)
            image3 = image3.resize((400, 360), Image.LANCZOS)
            photo3 = ImageTk.PhotoImage(image3)

            label3 = tk.Label(new_window, image=photo3)
            label3.image = photo3  # 保持對圖像的引用
            label3.pack(side=tk.LEFT, padx=(10,5), pady=5)

            # 圖片4
            image_path4 = r"C:\Users\user\Documents\GitHub\__11304_python_2024_tvdi__\homework\專案\波士頓房價預測_09_田恭豪\images\image_4.png"
            image4 = Image.open(image_path4)
            image4 = image4.resize((420, 360), Image.LANCZOS)
            photo4 = ImageTk.PhotoImage(image4)

            label4 = tk.Label(new_window, image=photo4)
            label4.image = photo4  # 保持對圖像的引用
            label4.pack(side=tk.RIGHT, padx=(5,10), pady=5)

        except FileNotFoundError as e:
            messagebox.showerror("錯誤", f"找不到指定的圖片檔案：{e}")

    def on_close(self):
        if messagebox.askokcancel("退出", "確定要退出嗎？"):
            self.destroy()

    def show_rating_dialog(self):
        # 準備要顯示的準確率數據
        knn_accuracy = analysis.max_knn_accuracy
        gs_accuracy = analysis.max_gs_accuracy
        dec_accuracy = analysis.max_dec_accuracy

        # 構建消息框顯示內容
        message = f"K近鄰模組_準確率：{knn_accuracy}\n\n"
        message += f"GridSearchCV網格搜索模組_準確率：{gs_accuracy}\n\n"
        message += f"決策樹分析_準確率：{dec_accuracy}"

        # 使用消息框顯示準確率
        messagebox.showinfo("模型準確率", message)

if __name__ == "__main__":
    window = MyWindow()
    window.mainloop()