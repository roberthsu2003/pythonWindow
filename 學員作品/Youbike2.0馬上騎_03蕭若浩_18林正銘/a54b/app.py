import requests
import pywifi
from pywifi import const
import time

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