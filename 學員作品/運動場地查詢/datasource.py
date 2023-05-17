import requests

def getInfo():
    global area_list,data_list,type_list
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    url = 'https://vbs.sports.taipei/opendata/sports_tms.json'
    response = requests.get(url, headers=header)
    data_list = response.json()
    area_temp = set()
    type_temp = set()
    for item in data_list:
        area_temp.add(item['Area'])
    area_list = sorted(list(area_temp))
    del area_list[0]
    for item in data_list:
        type_temp.add(item['SportType'])
    type_list = sorted(list(type_temp))
    del type_list[0]

def getInfoFromArea(areaname):
    filter_data = filter(lambda n:n['Area']==areaname,data_list)
    return list(filter_data)

getInfo()