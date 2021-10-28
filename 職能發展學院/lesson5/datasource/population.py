'''
解析各鄉鎮市區人口密度.csv
'''

import csv

csvfile = open('./datasource/各鄉鎮市區人口密度.csv',mode='r',encoding='utf-8',newline='')
csvReader = csv.reader(csvfile)
csvReader.__next__()
csvReader.__next__()
populations = list(csvReader)
populations = populations[0:-5] #後面5行不要

