import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import datasource as ds
import tkintermapview  # 地圖
import os
import pandas as pd
from tkinter import PhotoImage
from PIL import Image, ImageTk


# 標籤
class TKLable(tk.Label):
    def __init__(self, parents, **kwargs):
        super().__init__(parents, **kwargs)
        helv26 = tkFont.Font(family="微軟正黑體", size=12, weight="bold")
        self.config(font=helv26)


# 一般按鈕
class TKButton(tk.Button):
    def __init__(self, parents, **kwargs):
        super().__init__(parents, **kwargs)
        self.config(font=("微軟正黑體", 10, "bold"))


# 主視窗設定
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg="#345678")

        title = tk.Label(self, text="Fish", bg="#345678")
        titlefont = tkFont.Font(family="微軟正黑體", size=36, weight="bold")
        title.config(font=titlefont, foreground="#FFFFFF")
        title.pack(padx=10, pady=10)

        self.KeywordFrame = ttk.Frame(self, width=800, height=500)
        self.KeywordFrame.pack(fill="both", expand=True)

        mainFrame = tk.Frame(self.KeywordFrame, width=800, height=500)
        mainFrame.pack()

        TKLable(
            mainFrame,
            text="請使用下方列表,選取您想查詢的物件",
            bd=3,
        ).grid(row=0, column=0, columnspan=10, pady=5)

        # 原生種判定下拉選單
        TKLable(mainFrame, text="原生種判定", bd=1).grid(row=1, column=0)
        self.FishType_dict = ds.Get_FISHTYP()
        self.FishTypeValue = tk.StringVar()
        self.FishType_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishType_dict.keys()),
            justify="center",
            textvariable=self.FishTypeValue,
        )
        self.FishType_Combo.grid(row=1, column=1)
        self.FishType_Combo.current(0)
        # 下拉選單綁定Function
        self.FishType_Combo.bind("<<ComboboxSelected>>", self.update_FishName_Combo)

        # 年度下拉選單
        TKLable(mainFrame, text="年度", bd=1).grid(row=1, column=2)
        self.FishYear_dict = ds.Get_FISHYEAR()
        self.FishYearValue = tk.StringVar()
        self.FishYear_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishYear_dict.keys()),
            justify="center",
            textvariable=self.FishYearValue,
        )
        self.FishYear_Combo.grid(row=1, column=3)
        self.FishYear_Combo.current(0)

        # 地圖標記下拉選單
        '''TKLable(mainFrame, text="地圖標記", bd=1).grid(row=1, column=4)
        self.FishMap_dict = ds.Get_MAP()
        self.FishMapValue = tk.StringVar()
        self.FishMap_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishMap_dict.keys()),
            justify="center",
            textvariable=self.FishMapValue,
        )
        self.FishMap_Combo.grid(row=1, column=5)
        self.FishMap_Combo.current(0)'''

        # 中文名下拉選單
        TKLable(mainFrame, text="中文名", bd=3).grid(row=1, column=6)
        self.FishName_dict = ds.Get_FISHNAME()
        self.FishNameValue = tk.StringVar()
        self.FishName_Combo = ttk.Combobox(
            mainFrame,
            values=list(self.FishName_dict.keys()),
            justify="center",
            textvariable=self.FishNameValue,
        )
        self.FishName_Combo.grid(row=1, column=7)
        self.FishName_Combo.current(0)

        # 搜尋按鈕
        self.keyButton = TKButton(mainFrame, text="搜尋", command=self.KeySearch)
        self.keyButton.config(width=80, border=3)

        self.keyButton.grid(row=4, column=0, columnspan=10, pady=(5, 0), sticky="nsew")

        # Map 地圖
        map_box = tk.Canvas(self.KeywordFrame)  # 創建地圖框架
        map_box.pack(fill="both", expand=True, pady=10, padx=100)
        # 創建地圖
        self.map_widget = tkintermapview.TkinterMapView(
            map_box, width=100, height=800, corner_radius=0
        )
        # 引進地圖Function
        # 變更mark圖示
        self.current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.Mark_image = ImageTk.PhotoImage(
            Image.open(os.path.join(self.current_path, "colordot.png")).resize((50, 50))
        )
        # 地圖Fuction

        self.map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.pack(fill="both", expand=True, pady=5, padx=80)
        self.map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22
        )
        # 設置初始座標(中部)
        self.map_widget.set_position(23.623468547617622, 120.89823983585597)
        self.map_widget.set_zoom(8)
        #地圖標籤 右鍵
        # self.map_widget.add_right_click_menu_command(
        #    label="Add Marker", command=self.add_marker_event, pass_coords=True)
    
    # 搜尋條件
    def KeySearch(self) -> list[list]:
        aa=0
        
        # print(type(self.FishYearValue))
        # print(type(self.FishTypeValue))
        # print(type(self.FishNameValue))
        
        self.map_widget.delete_all_marker()  # 刪除舊的標點

        # Search定義
        fishtype = ""  # 原生種名稱
        fishyear = ""  # 年度
        #fishyear = str(fishyear1)
        fishname = ""  # 中文名
        """
        if self.FishTypeValue.get() != "全部":
            fishtype = str(self.FishTypeValue.get())
        if self.FishYearValue.get() != "全部":
            fishyear = int(self.FishYearValue.get())
        if self.FishNameValue.get() != "全部":
            fishname = str(self.FishNameValue.get())
        """
        if self.FishTypeValue.get() != "全部":
            fishtype = str(self.FishTypeValue.get())
        if self.FishNameValue.get() != "全部":
            fishname = str(self.FishNameValue.get())
        #if self.FishYearValue.get() != "全部":
        #    fishyear = str(self.FishYearValue.get())

        # 处理 FishYearValue
        try:
            fishyear = int(self.FishYearValue.get())
        except (ValueError, tk.TclError):
            print("Invalid value for fish year")
            fishyear = None

        # 用pandas 讀取 csv 檔
        df = pd.read_csv("Pie_data.csv", encoding="utf-8", low_memory=False)
        
        for item in df.iterrows():
            fishtypecheck = False
            fishyearcheck = False
            fishnamecheck = False

            name = item[1]["中文名"]
            type = item[1]["原生種判定"]
            year = (item[1]["年度"])
            count = item[1]["數量(隻)"]
            where = item[1]["水系"]
            x = float(item[1]["Latitude"])
            y = float(item[1]["Longitude"])

            # print(item[1]["中文名"])
            # print(item[1]["Longitude"])
            # print(item[1]["Latitude"])
            # print("=================")
            # 要先查資料類型
            if fishtype == "" and fishyear == "" and fishname == "":
                aa += 1    
                self.map_widget.set_marker(x, y, icon=self.Mark_image)          
                if aa==1:
                    print("break4")
                    break
            if fishtype =="" and fishname == "" or fishtype =="" and fishyear == "" or fishname =="" and fishyear == ""  :
                aa += 1
                self.map_widget.set_marker(x, y, icon=self.Mark_image)
                if aa == 1:
                    print("break3")
                    break
            if fishtype == "" or fishyear == "" or fishname == "":
                aa += 1
                fishyear = int(self.FishYearValue.get())
                self.map_widget.set_marker(x, y, icon=self.Mark_image)
                if aa == 5:
                    print("break2")
                    break
            if item[1]["中文名"] == fishname:
                fishyear = int(self.FishYearValue.get())
                aa += 1
                self.map_widget.set_marker(x, y, icon=self.Mark_image)
                
                if aa == 2:
                    print("break1")
                    break

    #下拉選單連結Function
    def update_FishName_Combo(self, event):
        selected_tag = self.FishType_dict[self.FishTypeValue.get()]
        # 根据第一个下拉菜单的选项更新第二个下拉菜单的选项

        if (self.FishTypeValue.get()) == "全部":
            filtered_names = [name for name, tag in self.FishName_dict.items()]
            self.FishName_Combo["values"] = filtered_names
        else:
            filtered_names = [
                name for name, tag in self.FishName_dict.items() if tag == selected_tag
            ]
            self.FishName_Combo["values"] = filtered_names
            self.FishName_Combo.current(0)
        self.FishNameValue.set("全部")
    #地圖右鍵Function
    # def add_marker_event(coords):
    #   print("Add marker:", coords)
    # new_marker = map_widget.set_marker(coords[0], coords[1], text="new marker")


def main():
    window = Window()
    window.title("Fish")  # title
    window.resizable()  # 禁止拖拉視窗調整視窗大小
    window.geometry("1000x900")  # 視窗大小
    window.mainloop()


if __name__ == "__main__":
    main()
