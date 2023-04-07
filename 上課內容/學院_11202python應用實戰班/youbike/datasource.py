import requests

sarea_list = None
data_list = None

def getInfo():
    global sarea_list,data_list
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    data_list = response.json()
    sarea_temp = set()
    for item in data_list:
        sarea_temp.add(item["sarea"])
    sarea_list = sorted(list(sarea_temp))

def getInfoFromArea(areaName):
    filter_data = filter(lambda n:n["sarea"]==areaName,data_list)
    return list(filter_data)
    

getInfo()