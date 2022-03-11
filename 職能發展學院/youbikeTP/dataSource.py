import requests
from requests import ConnectionError,HTTPError,Timeout
import sqlite3
from sqlite3 import Error as sqlite3Error

__all__ = ['update_youbike_data']

def download_youbike_data():
    youbikeurl = "https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json"
    try:
        response = requests.get(youbikeurl)
        response.raise_for_status()
    except ConnectionError as e:
        print("網路連線有問題")
        print(e)
        return
    except HTTPError as e:
        print("statusCode不是200,連線取得資料有問題")
        print(e)
        return
    except Timeout as e:
        print("伺服器忙線中")
        print(e)
        return
    except:
        print("不預期的錯誤")
        return

    allData = response.json()
    #解析資料,傳出[{:}]
    return list(allData["retVal"].values())

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3Error as e:
        print("sqlite連線錯誤")
        print(e)
        return
    return conn

def create_youbike_table(conn):
    sql = '''
    CREATE TABLE IF NOT EXISTS youbike(
    id INTEGER PRIMARY KEY,
    sno TEXT NOT NULL,
    sna TEXT NOT NULL,
    tot INTEGER,
    sbi INTEGER,
    sarea TEXT,
    mday TEXT,
    lat REAL,
    lng REAL,
    ar TEXT,
    bemp INTEGER,
    act INTEGER,
    UNIQUE (sno)
);
    '''

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except sqlite3Error as e:
        print(e)


def replace_youbike_data(conn,dataList):
    from datetime import datetime
    def change_mday_string_format(mday):
        datetimeObject = datetime.strptime(mday,"%Y%m%d%H%M%S")
        return datetimeObject.strftime("%Y-%m-%d %H:%M:%S")

    sql = '''
    INSERT or replace  INTO 
    youbike(sno,sna,tot,sbi,sarea,mday,lat,lng,ar,bemp,act)
    VALUES( ?,?,?,?,?,?,?,?,?,?,?)
    '''

    try:
        curser = conn.cursor()
        for item in dataList:
            sno = item['sno']
            sna = item['sna']
            tot = int(item['tot'])
            sbi = int(item['sbi'])
            sarea = item['sarea']
            mday = change_mday_string_format(item['mday']);
            lat = float(item['lat'])
            lng = float(item['lng'])
            ar = item['ar']
            bemp = int(item['bemp'])
            act = int(item['act'])
            curser.execute(sql,(sno,sna,tot,sbi,sarea,mday,lat,lng,ar,bemp,act))
    except  sqlite3Error as e:
        print(e)

    conn.commit()





def update_youbike_data():
    datalist = download_youbike_data()
    conn = create_connection('youbike.db')
    with conn:
        create_youbike_table(conn)
        replace_youbike_data(conn,datalist)

'''
SELECT sno as 站點編號,sna as 站點名稱,tot as 總容量,sbi as 可借,bemp as 可還,act as 狀態
FROM youbike
WHERE act = 1 AND sbi > 3 AND bemp >3
'''

'''
SELECT count(*) as 正常數量
FROM youbike
WHERE act = 1 AND sbi > 3 AND bemp >3
'''


