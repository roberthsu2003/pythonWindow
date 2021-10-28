'''
解析各鄉鎮市區人口密度.csv
提供資料
'''

import csv

csvfile = open('./datasource/各鄉鎮市區人口密度.csv',mode='r',encoding='utf-8',newline='')
csvReader = csv.reader(csvfile)
csvReader.__next__()
csvReader.__next__()
populations = list(csvReader)
populations = populations[0:-5] #後面5行不要

def getNum(item):
    try:
        return int(item)
    except:
        return 0

def get_populations():
    total = 0
    for item in populations:
        itemNum = getNum(item[2])
        total += itemNum
    return total

def getFloat(item):
    try:
        return float(item)
    except:
        return 0.0

def get_areas():
    areas = 0.0
    for item in populations:
        floatNum = getFloat(item[3])
        areas += floatNum
    return areas

def get_listNum():
    return len(populations)
