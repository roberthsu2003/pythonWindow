import requests
from io import StringIO
import csv

airportname_list = None
data_list = None

def getInfo():
    global airportname_list, data_list
    response = requests.get('https://www.taoyuan-airport.com/uploads/govdata/FidsPassenger.csv')
    file = StringIO(response.text,newline='')
    csvReader = csv.DictReader(file)
    data_list = list(csvReader)
    airportname_temp = set()
    for item in data_list:
        airportname_temp.add(item['航空公司中文'].strip())
    airportname_list = sorted(list(airportname_temp))


def getInfoFromAirPort(areaName) -> list:
    filter_data = filter(lambda n:n['航空公司中文'].strip()==areaName.strip(),data_list)
    return list(filter_data)

getInfo()