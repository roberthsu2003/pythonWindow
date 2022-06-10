from tkinter.simpledialog import Dialog
import tkintermapview as tkmap
import tkinter as tk

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




    def body(self, master):
        map_widget = tkmap.TkinterMapView(master,
                                          width=800,
                                          height=600,
                                          corner_radius=0
                                          )
        centerLat,centerLong = self.getCenter()

        map_widget.set_position(centerLat, centerLong)  # 台北市位置
        map_widget.set_zoom(15)  # 設定顯示大小
        map_widget.pack()

        #建立marker
        for site in self.info:
            marker = map_widget.set_marker(site['lat'],site['lng'],command=self.click1)
            marker.data = site

    def click1(self,marker):
        marker.text = marker.data['sna']



    def buttonbox(self):
        #super().buttonbox()
        #自訂按鈕區
        bottomFrame = tk.Frame(self)
        tk.Button(bottomFrame,text="關閉"+self.title()+"地圖",command=self.ok,padx=10,pady=10).pack(padx=10,pady=20)
        bottomFrame.pack()


    def ok(self, event=None):
        super().ok()


