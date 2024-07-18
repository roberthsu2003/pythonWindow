from flask import Flask, render_template
import requests
import pywifi
import time

app = Flask(__name__)

def dload_json():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    try:
        res = requests.get(url)
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return []
    return res.json()

def get_wifi_access_points():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    if not interfaces:
        print("No WiFi interfaces found")
        return []
    iface = interfaces[0]
    iface.scan()
    time.sleep(2)  # 等待扫描完成
    return iface.scan_results()

def get_geolocation(api_key, wifi_access_points):
    if not wifi_access_points:
        print("No WiFi access points found")
        return None

    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"
    payload = {
        "wifiAccessPoints": [{"macAddress": ap.bssid, "signalStrength": ap.signal} for ap in wifi_access_points]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 403:
        print("Access forbidden: Check your API key and service restrictions.")
        return None
    elif response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json().get('location', None)

@app.route('/')
def index():
    API_KEY = 'AIzaSyBp5glOERo1EPg_9boiCdweZuwp-tEgp1o'
    wifi_access_points = get_wifi_access_points()
    location = get_geolocation(API_KEY, wifi_access_points)
    
    if location:
        latitude, longitude = location['lat'], location['lng']
    else:
        latitude, longitude = 0, 0
        print("Using default latitude and longitude")

    all_datas = dload_json()
    
    filtered_data = [
        {
            'sna': dat.get('sna', '未知'),
            'sarea': dat.get('sarea', '未知'),
            'mday': dat.get('mday', '未知'),
            'ar': dat.get('ar', '未知'),
            'total': dat.get('total', 0),
            'rent_bikes': dat.get('available_rent_bikes', 0),
            'retuen_bikes': dat.get('available_return_bikes', 0)
        }
        for dat in all_datas if abs(dat.get('latitude', 0) - latitude) < 0.00350 and abs(dat.get('longitude', 0) - longitude) < 0.00350
    ]
    
    return render_template('index.html', data=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
