import requests

# Store the area names and data
sarea_list = None
data_list = None

def getInfo() -> None:
    # Get data from TCGB website
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    data_list = response.json()
    # Get all available areas
    sarea_temp = set()
    for item in data_list:
        sarea_temp.add(item["sarea"])
    sarea_list = sorted(list(sarea_temp))

def getInfoFromArea(areaName) -> list:
    filter_data = filter(lambda n:n["sarea"]==areaName,data_list)
    return list(filter_data)
    
def filter_sbi_warning_data(area_data,numbers) -> list:
    filter_data = filter(lambda n:n['sbi']<=numbers,area_data)
    return list(filter_data)

def filter_bemp_warning_data(area_data, numbers) -> list:
    filter_data = filter(lambda n: n['bemp'] <= numbers, area_data)
    return list(filter_data)

getInfo()