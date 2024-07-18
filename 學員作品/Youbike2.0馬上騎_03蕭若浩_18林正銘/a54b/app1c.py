import requests
import pywifi
from pywifi import const
import time
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox,Misc
import data
from data import FilterData,Info
from tools import CustomMessagebox
from requests import Response
from pydantic import BaseModel, RootModel, Field
from pydantic import BaseModel, RootModel, Field,field_validator,ConfigDict
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
mydata1:list[dict] = []

class Window(ThemedTk):
    def __init__(self,theme:str='arc',**kwargs):
        super().__init__(theme=theme,**kwargs)
        global mydata1
        print(len(mydata1))
        print(type(mydata1))
        self.title('台北市YouBike2.0及時資料_python小組專題_3&18_MAP')
        try:
            #self.__data = data.load_data()
            self.__data = mydata1
        except Exception as e:
            messagebox.showwarning(title='警告',message=str(e))
        
        self._display_interface()
        
    @property
    def data(self)->list[dict]:
        return self.__data
    

    def _display_interface(self):
        mainFrame = ttk.Frame(borderwidth=1,relief='groove')
        ttk.Label(mainFrame,text="台北市YouBike2.0及時資料_python小組專題_3&18_MAP",font=('arial',25)).pack(pady=(20,10))
        #=================================
        tableFrame = ttk.Frame(mainFrame)
        columns = ('sna', 'sarea', 'mday','ar','total','rent_bikes','retuen_bikes')
        tree = ttk.Treeview(tableFrame, columns=columns, show='headings',selectmode='browse')
        # define headings
        tree.heading('sna', text='站點')
        tree.heading('sarea', text='行政區')
        tree.heading('mday', text='時間')
        tree.heading('ar', text='地址')
        tree.heading('total', text='總數')
        tree.heading('rent_bikes', text='可借')
        tree.heading('retuen_bikes', text='可還')

        # 定義欄位寬度
        tree.column('sarea',width=70,anchor=tk.CENTER)
        tree.column('mday',width=120,anchor=tk.CENTER)
        tree.column('ar',minwidth=100)
        tree.column('total',width=50,anchor=tk.CENTER)
        tree.column('rent_bikes',width=50,anchor=tk.CENTER)
        tree.column('retuen_bikes',width=50,anchor=tk.CENTER)

        # bind使用者的事件
        tree.bind('<<TreeviewSelect>>', self.item_selected)


        
        
        # add data to the treeview
        for site in self.data:
            tree.insert('', tk.END,
                        values=(site['sna'],site['sarea'],site['mday'],site['ar'],site['total'],site['rent_bikes'],site['retuen_bikes']))
        
        tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tableFrame.pack(expand=True,fill=tk.BOTH,padx=20,pady=20)
        #======================================
        mainFrame.pack(expand=True,fill=tk.BOTH,padx=10,pady=10)

    def item_selected(self,event):
        tree = event.widget
        print(isinstance(tree,ttk.Treeview))
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record:list = item['values']
            site_data:Info = FilterData.get_selected_coordinate(sna=record[0],data=self.data)
            CustomMessagebox(self,title=site_data.sna,site=site_data)
            


def dload_json():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    try:
        res:Response = requests.get(url)
    except Exception:
        raise("連線失敗")
    else:
        all_datas:dict[any] = res.json()
        return all_datas

def get_wifi_access_points():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)  # 等待扫描完成
    scan_results = iface.scan_results()
    
    wifi_access_points = []
    for ap in scan_results:
        ap_info = {
            "macAddress": ap.bssid,
            "signalStrength": ap.signal
        }
        wifi_access_points.append(ap_info)
    
    return wifi_access_points

def get_geolocation(api_key, wifi_access_points):
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"
    payload = {
        "wifiAccessPoints": wifi_access_points
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 403:
        print("Access forbidden: Check your API key and service restrictions.")
        print(response.json())
        return None
    elif response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

    location_data = response.json()
    return location_data['location']

def main():
    global mydata1
    def on_closing():
        print("手動關閉視窗")
        window.destroy()
        window.quit()
    # 你的 Google Geolocation API 密钥
    API_KEY = 'AIzaSyBp5glOERo1EPg_9boiCdweZuwp-tEgp1o'

    wifi_access_points = get_wifi_access_points()
    print(f"Detected WiFi Access Points: {wifi_access_points}")

    location = get_geolocation(API_KEY, wifi_access_points)
    if location:
        latitude = location['lat']
        longitude = location['lng']
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Failed to get location data.")

    try:
        all_datas:dict[any] = dload_json()
    except Exception as error:
        print(error)
    #print(all_datas)

    #from pydantic import BaseModel, RootModel, Field

    class Info(BaseModel):
        sna:str
        sarea:str
        mday:str
        ar:str
        act:str
        updateTime:str
        total:int
        rent_bikes:int = Field(alias="available_rent_bikes")
        lat:float = Field(alias="latitude")
        lng:float = Field(alias="longitude")
        retuen_bikes:int = Field(alias="available_return_bikes")

    class ubike_Data(RootModel):
        root:list[Info]
    ubike_data:ubike_Data = ubike_Data.model_validate(all_datas)
    mydata = ubike_data.model_dump()

    import math
    global mydata1
    for dat in mydata:
        if abs(float(dat['lat'] - latitude)) < 0.00350 and abs(float(dat['lng'] - longitude)) < 0.00350:
            print(dat['lat'] - latitude)
            print(dat['lng'] - longitude) 
            print(dat['lat'])
            print(dat['lng']) 
            print(dat['sna'])
            print(dat['sarea'])
            print(dat['ar'])
            print(dat['act'])
            print(dat['rent_bikes'])
            print(dat['retuen_bikes'])
            print(type(dat))
            mydata1.append(dat)
            print((mydata1))
            print(type(mydata1))
        

    window = Window(theme='breeze')
    window.mainloop()

if __name__ == '__main__':
    main()