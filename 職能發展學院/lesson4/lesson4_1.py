#!/usr/bin/python3.10
import requests
import sqlite3
from sqlite3 import Error

urlpath = '	https://data.epa.gov.tw/api/v1/aqx_p_02?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&sort=ImportDate%20desc&format=json'

def create_connection(db_file):
    """
    連線至資料庫
    :param db_file: 資料庫的檔案名稱
    :return: Connection物件
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        return

    return conn

def stringToFloat(s):
    try:
       return float(s)
    except:
        return 999.0

def saveToDataBase(datas):
    '''
    儲存資料至資料庫db25
    :param datas: list->tuple
    :return:
    '''
    conn = create_connection('pm25.db')
    print("資料庫連線成功")

def downloadData():
    response = requests.get(urlpath)
    if response.status_code == 200:
        print('下載成功')
        data = response.json()
        datas = data["records"]
        importData = [
            (item['Site'], item['county'], stringToFloat(item['PM25']), item['DataCreationDate'], item['ItemUnit']) for
            item in datas]
        return importData

def main():
    importData = downloadData()
    saveToDataBase(importData)

if __name__ == '__main__':
    main()