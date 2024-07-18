import requests
import pywifi
from pywifi import const
import time
from requests import Response
from pydantic import BaseModel, RootModel, Field
#from pydantic import BaseModel, RootModel, Field,field_validator,ConfigDict

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
mydata1:list[dict] = []
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