from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
import modules.all_data as all_data
import webbrowser
import modules.tool as tool
import random
from PIL import Image, ImageTk

class Window(ThemedTk):
    def __init__(self,theme="arc", **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.iconphoto(False, tk.PhotoImage(file = "./images/rest_and_map_icon.png"))
        self.title("今天要吃什麼")
        self.geometry('800x500')
        self.resizable(False, False)
        
        # 創建 StringVar 物件
        self.combobox_country= tk.StringVar()
        self.updating = False

        # 創建IntVar()物件
        self.update_value = tk.IntVar(value=100)
        self.widgets()

    # widgets Layout
    def widgets(self):
        mainFrame = ttk.Frame(borderwidth=1, relief='groove')
        county:list = all_data.twn_county()

        # 下拉式選單
        style = ttk.Style()
        style.configure("TCombobox", foreground="black")
        city_label = ttk.Label(mainFrame, text="請選擇(縣/市):") 
        self.select_city = ttk.Combobox(mainFrame, textvariable= self.combobox_country, values = county, state='readonly', width=18, style="TCombobox")
        # 初始值顯示台北市
        self.select_city.current(0)

        # 輸入地址
        address_label = ttk.Label(mainFrame, text="請輸入地址:")
        self.entry_address = ttk.Entry(mainFrame, width=20, foreground="black")
        self.entry_address.focus()

        # 距離範圍, 數值調整滑桿
        distance_label = ttk.Label(mainFrame, text="調整搜尋範圍:")
        self.distance_scale= ttk.Scale(mainFrame, from_=100, to=3000, orient='horizontal', length=186, command=self.update_distance_value)
        self.distance_scale.set(100)
        
        # self.update_value.set(100)
        self.scale_value_label = ttk.Label(mainFrame, textvariable=self.update_value)
        m_lable = ttk.Label(mainFrame, text="公尺")
        
        # 查詢
        self.search_btn = ttk.Button(mainFrame, text="查詢", command=self.submit_address)

        # 隨機選擇一家餐廳
        self.random_restaurant_btn= ttk.Button(mainFrame, text="隨機餐廳", command=self.show_random_restaurant)

        # 清除entry & Treeview 值
        self.clear_btn = ttk.Button(mainFrame, text="清除", command=self.clear_entry_and_treeview)
        
        # 建立Treeview
        tableFrame = ttk.Frame(self, borderwidth=1, relief='groove')
        columns = ('restaurant_id', 'restaurant_name', 'rating', 'user_ratings_total', 'price_level', 'address', 'phone_number')
        # 設定成 browse(只能單選)
        self.tree = ttk.Treeview(tableFrame, columns=columns, show='headings', selectmode='browse')

        # define headings
        self.tree.heading('restaurant_id', text='編號')
        self.tree.heading('restaurant_name', text='餐廳名稱')
        self.tree.heading('rating', text='餐廳評分')
        self.tree.heading('user_ratings_total', text='評論數')
        self.tree.heading('price_level', text='消費金額')
        self.tree.heading('address', text='地址')
        self.tree.heading('phone_number', text='電話')

        # 定義欄位寬度
        self.tree.column('restaurant_id', width=100, anchor='center')
        self.tree.column('restaurant_name', minwidth=100, anchor='center')
        self.tree.column('rating', width=100, anchor='center')
        self.tree.column('user_ratings_total', width=100, anchor='center')
        self.tree.column('price_level', width=130, anchor='center')
        self.tree.column('address', minwidth=300, anchor='center')
        self.tree.column('phone_number', width=250, anchor='center')

        # 垂直 ＆ 水平 滾動條
        tree_scroll_y = ttk.Scrollbar(tableFrame, orient="vertical", command=self.tree.yview)
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = ttk.Scrollbar(tableFrame, orient="horizontal", command=self.tree.xview)
        tree_scroll_x.pack(side="bottom", fill="x")
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        # 綁定Treeview點擊事件
        self.tree.bind('<ButtonRelease-1>', self.tree_select)
     
        # 追蹤隨機餐廳視窗的狀態
        self.random_window_open = False

        # pack & grid
        mainFrame.pack(ipadx=150, ipady=10)
        city_label.grid(column=0, row=0, sticky="w", padx=(200,0), pady=(10, 5))
        self.select_city.grid(column=1, row=0, sticky="w", padx=(10,0), pady=(10, 5))
        address_label.grid(column=0, row=1, sticky="w", padx=(200,0), pady=(5, 5))
        self.entry_address.grid(column=1, row=1, sticky="w", padx=(10,0), pady=(5, 5),)
        distance_label.grid(column=0, row=2, sticky="w", padx=(200,0), pady=(5, 5))
        self.distance_scale.grid(column=1,row=2, sticky="w", padx=(10,0), pady=(5, 5))
        self.scale_value_label.grid(column=2,row=2, pady=(5, 5))
        m_lable.grid(column=3,row=2, pady=(5, 5))
        self.clear_btn.grid(column=0,row=3, sticky="w", padx=(200,0), pady=(5, 5))
        self.random_restaurant_btn.grid(column=1,row=3, padx=(10,0), pady=(5, 5))
        self.search_btn.grid(column=2,row=3, sticky="e", padx=(10,0), pady=(5, 5))

        tableFrame.pack(fill="both", expand=True)
        self.tree.pack(fill="both", expand=True)
        
    # 數值調整滑桿，加50 
    def update_distance_value(self, value):
        
        # 如果正在更新中
        if self.updating:  
            return 
        # 正在更新的狀態
        self.updating = True
        try:
            rounded_value = round(float(value) / 50) * 50
            self.update_value.set(int(rounded_value))
            self.distance_scale.set(rounded_value)
        finally:
            # 更新结束，恢復更新狀態 False
            self.updating = False  

    # 輸入地址，從呼叫data，抓資料
    def submit_address(self):

        combobox_value = self.combobox_country.get()
        entry_value = self.entry_address.get().strip()
        distance_value = int(self.distance_scale.get())
        address = combobox_value + entry_value

        if not entry_value:
            messagebox.showwarning("輸入錯誤", "地址欄位不能為空白，請重新輸入！")
        else:
            lat, lng= all_data.input_address(address)
            self.restaurants:list = all_data.get_nearby_restaurants(lat, lng, distance_value)
            self.insert_data(self.restaurants)
    
    # 將資料寫入到treeview內
    def insert_data(self, restaurants):

        # 清除現有數據
        for info in self.tree.get_children():
            self.tree.delete(info)

        # 將餐廳資料寫入
        for restaurant in restaurants:
                value = ( restaurant['restaurant_id'],
                          restaurant['restaurant_name'],
                          restaurant['rating'],
                          restaurant['user_ratings_total'],
                          restaurant['price_level'],
                          restaurant['address'],
                          restaurant['phone_number'],
                          restaurant['website'],
                          restaurant['place_id'],
                          restaurant['photo_url']
                        )
                
                self.tree.insert('', tk.END, values=value)

    # treeview 事件, 點擊到的餐廳連接 Google Maps query URL 
    def tree_select(self, event):

        selected_items = self.tree.selection()
        if not selected_items:
            return  
        
        gmaps = all_data.gmaps
        selected_item = self.tree.selection()[0]
        restaurant_details = self.tree.item(selected_item, 'values')
        address = restaurant_details[5]
        geocode_result = gmaps.geocode(address)

        if not geocode_result:
            messagebox.showerror("錯誤", "無法獲取地理編碼，請檢查地址是否正確！")
            return
        
        place_id = restaurant_details[8]
    
        # Google Maps query URL
        URL = f"https://www.google.com/maps/search/?api=1&query={address}&query_place_id={place_id}"
        
        # 開啟預設瀏覽器
        webbrowser.open(URL)
    
    # 隨機選取一個餐廳，並顯示在新視窗上
    def show_random_restaurant(self):
        
        if not self.tree.get_children():
            messagebox.showwarning("警告", "表格中沒有餐廳資料!  請重新查詢～")
            return

        if self.random_window_open:
            messagebox.showwarning("提示", "隨機餐廳視窗已經開啟！")
            return
        
        # 標記為已打開隨機餐廳視窗
        self.random_window_open = True

        # 隨機選擇一個餐廳
        random_restaurant = random.choice(self.restaurants)
        
        # 創建一個新窗口來顯示餐廳資訊和圖片
        new_window = tk.Toplevel(self)
        new_window.iconphoto(False, tk.PhotoImage(file = "./images/rest_and_map_icon.png"))
        new_window.title(random_restaurant['restaurant_name'])

        # 抓取餐廳的照片的url
        photo_url = random_restaurant['photo_url']

        # 顯示照片
        if photo_url:
            try:
                # 讀取url和顯示照片
                image_byt = tool.get_image(photo_url)
                image_b64 = tool.decode_image(image_byt)
                image = Image.open(image_b64)
                self.photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(new_window, image=self.photo)
                image_label.pack()
                # 監聽視窗關閉事件，標記隨機餐廳視窗已關閉
                new_window.protocol("WM_DELETE_WINDOW", lambda: self.random_window_close(new_window))
            except Exception as e:
                error_label = ttk.Label(new_window, text="圖片加載失敗", justify=tk.LEFT, foreground="red")
                error_label.pack(fill='both', expand=True)
                # 監聽視窗關閉事件，標記隨機餐廳視窗已關閉
                new_window.protocol("WM_DELETE_WINDOW", lambda: self.random_window_close(new_window))
        
        # 顯示餐廳資訊
        new_window_frame = ttk.Frame(new_window)
        new_window_frame.pack(fill='both', expand=True)
        # 設置列的權重，讓列在水平上可擴展
        new_window_frame.columnconfigure(0, weight=1)

        ttk.Label(new_window_frame, text="餐廳資訊", font=("微軟正黑體", 20)).grid(column=0, row=0, sticky="n", pady=(10,0))
        ttk.Label(new_window_frame, text=f"編號: {random_restaurant['restaurant_id']}", font=("微軟正黑體", 16)).grid(column=0, row=1, sticky="w", padx=20, pady=(10, 5), ipadx=5)
        ttk.Label(new_window_frame, text=f"餐廳名稱: {random_restaurant['restaurant_name']}", font=("微軟正黑體", 16)).grid(column=0, row=2, sticky="w", padx=20, pady=(0, 5), ipadx=5)
        ttk.Label(new_window_frame, text=f"評分: {random_restaurant['rating']}", font=("微軟正黑體", 16)).grid(column=0, row=3, sticky="w", padx=20, pady=(0, 5), ipadx=5)
        ttk.Label(new_window_frame, text=f"評論數: {random_restaurant['user_ratings_total']}", font=("微軟正黑體", 16)).grid(column=0, row=4, sticky="w", padx=20, pady=(0, 5), ipadx=5)
        ttk.Label(new_window_frame, text=f"消費金額: {random_restaurant['price_level']}", font=("微軟正黑體", 16)).grid(column=0, row=5, sticky="w", padx=20, pady=(0, 5), ipadx=5)
        ttk.Label(new_window_frame, text=f"地址: {random_restaurant['address']}", font=("微軟正黑體", 16)).grid(column=0, row=6, sticky="w", padx=20, pady=(0, 5), ipadx=5)
        ttk.Label(new_window_frame, text=f"電話: {random_restaurant['phone_number']}", font=("微軟正黑體", 16)).grid(column=0, row=7, sticky="w", padx=20, pady=(0, 20), ipadx=5)
    
    # 事件關閉隨機餐廳視窗
    def random_window_close(self, new_window):
        # 視窗關閉時
        new_window.destroy()
        # 標記隨機餐廳視窗已關閉
        self.random_window_open = False
    
    # 清除視窗地址內容和餐廳資料
    def clear_entry_and_treeview(self):
        self.entry_address.delete(0, tk.END)

        # 清除 Treeview 內容
        for restaurant_info in self.tree.get_children():
            self.tree.delete(restaurant_info)

def main():
    window = Window()
    window.mainloop()

if  __name__ == '__main__':
    main()

