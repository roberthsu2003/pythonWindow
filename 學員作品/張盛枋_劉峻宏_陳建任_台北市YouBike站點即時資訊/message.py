from tkinter.simpledialog import Dialog
import tkintermapview 
import tkinter as tk
from tkinter import ttk,messagebox
import os
from PIL import Image, ImageTk

class MapDialog(Dialog):
    def __init__(self, parent, title = None,info=None):
        self.info = info
        super().__init__(parent,title=title)


    def getCenter(self):
        lat_l,lat_s,lng_l,lng_s = -10000,100000,-100000,100000
        for site in self.info:
            if lat_l < site["lat"]:
                lat_l = site["lat"]
            if lat_s > site["lat"]:
                lat_s = site["lat"]
            if lng_l < site["lng"]:
                lng_l = site["lng"]
            if lng_s > site["lng"]:
                lng_s = site["lng"]

        lat_cen = lat_s + ((lat_l - lat_s) / 2)
        lng_cen = lng_s + ((lng_l - lng_s) / 2)
        print(lat_cen)
        print(lng_cen)
        return lat_cen, lng_cen

    def MapSearch(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_bar.get()
            self.search_marker = self.map_widget.set_address(address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False

    def MapClear(self):
        """Clear the search bar and map."""
        self.search_bar.delete(0, last=tk.END)
        self.map_widget.delete(self.search_marker)

        # Get center coordinates of the markers
        center_lat, center_lng = self.getCenter()

        # Set map center to the calculated center
        self.map_widget.set_position(center_lat, center_lng)
        self.map_widget.set_zoom(14)

    def body(self, master):
        self.marker_list = []
        self.marker_path = None
        self.search_marker = None
        self.search_in_progress = False
        searchFrame = tk.Frame(master,width=800,height=200)
        searchFrame.pack()

        self.search_bar = tk.Entry(searchFrame, width=50)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        self.search_bar_button = tk.Button(master=searchFrame, width=8, text="搜尋", command=self.MapSearch)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_bar_clear = tk.Button(master=searchFrame, width=8, text="清除/重置", command=self.MapClear)
        self.search_bar_clear.grid(row=0, column=2, pady=10, padx=10)


        self.map_widget = tkintermapview.TkinterMapView(master,width=800, height=600, corner_radius=0)
        centerLat,centerLong = self.getCenter() # 各行政區中央位置的經緯度
        self.map_widget.pack(fill="both", expand=True)
        # self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=20)
        # 當 zoom >= 20，Google Map 的 YouBike站點 會顯示站點名稱，會跟我們的 marker text 重疊顯示。
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=19)
        # map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.set_position(centerLat, centerLong) # 將各行政區中央位置的經緯度，設定為地圖中心
        # self.map_widget.set_position(25.038263362662818, 121.52830359290476)  # 設置初始座標(東門約略在台北市中心)

        self.map_widget.set_zoom(14)

        # Load images for icon
        current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        Bike_image_B = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "Bike_Blue.png")).resize((35, 35)))
        Bike_image_R = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "Bike_Red.png")).resize((35, 35)))

        #建立marker
        for site in self.info:
            textcolor = '#FF5151' if site['sbi'] == 0 else '#0066CC'
            Bike_image = Bike_image_R if site['sbi'] == 0 else Bike_image_B

            marker = self.map_widget.set_marker(
                site['lat'],
                site['lng'],
                text_color=textcolor,
                font=('arial bold', 10),
                icon=Bike_image,
                command=self.click1
            )
            marker.data = site

#                text=f"{site['sna']}",

    def click1(self,marker):
        '''
        marker.text = marker.data['sna']
        marker.marker_color_outside='black'
        self.map_widget.set_position(marker.data['lat'], marker.data['lng'])
        '''
        '''
        Update marker text and color, and center the map on the marker's location.
        '''
        # Center the map on the marker's location
        marker.text = str(f"{marker.data['sna']}\n\t可借:{marker.data['sbi']}\n\t可還:{marker.data['bemp']}")
        lat, lng = marker.data['lat'], marker.data['lng']
        self.map_widget.set_position(lat, lng)
        self.map_widget.set_zoom(17)


    def center_map(self):
        lat_sum = 0
        lng_sum = 0
        num_markers = len(self.marker_list)

        for marker in self.marker_list:
            lat_sum += marker.lat
            lng_sum += marker.lng

        lat_avg = lat_sum / num_markers
        lng_avg = lng_sum / num_markers

        self.map_widget.set_position(lat_avg, lng_avg)


    def buttonbox(self):
        #super().buttonbox()
        #自訂按鈕區
        #'relief='邊框樣式，可以設定 flat[扁平]、sunken[凹陷]、raised[浮凸]、groove[邊框]、ridge、solid，預設 flat。 https://steam.oxxostudio.tw/category/python/tkinter/button.html#a3
        bottomFrame = tk.Frame(self)
        tk.Button(bottomFrame,text="關閉"+self.title()+"地圖",command=self.ok,padx=10,pady=10,activeforeground='#FFF',bg='#FFF',relief='raised').pack(padx=10,pady=(5,10))
        bottomFrame.pack()


    def ok(self, event=None):
        super().ok()