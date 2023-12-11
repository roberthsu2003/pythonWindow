import requests
import sqlite3

__all__ = ['updata_sqlite_data']

AREA = ["文山區","內湖區","南港區","萬華區","大安區","中正區","松山區","信義區","北投區","大同區","士林區","中山區","臺大公館校區"]
DATA = None

def __download_youbike_data()->list[dict]:
    '''
    下載台北市youbike資料2.0
    https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json
    '''
    youbike_url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    response = requests.get(youbike_url)
    response.raise_for_status()
    print("數據更新成功")
    return response.json()

def download():
    global DATA
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    if response.status_code == 200:
        DATA = response.json()

#執行一次
download()

def __create_table(conn:sqlite3.Connection):    
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE  IF NOT EXISTS 台北市youbike(
            "id"	INTEGER,
            "站點名稱"	TEXT NOT NULL,
            "行政區"	TEXT NOT NULL,
            "更新時間"	TEXT NOT NULL,
            "地址"	TEXT,
            "總車輛數"	INTEGER,
            "可借"	INTEGER,
            "可還"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT),
            UNIQUE(站點名稱,更新時間) ON CONFLICT REPLACE 
        );
        '''
    )
    conn.commit()
    cursor.close()
    print("Table建立中請稍後")

def __insert_data(conn:sqlite3.Connection,values:list[any])->None:
    cursor = conn.cursor()
    sql = '''
    REPLACE INTO 台北市youbike(站點名稱,行政區,更新時間,地址,總車輛數,可借,可還)
        VALUES(?,?,?,?,?,?,?)
    '''
    cursor.execute(sql,values)    
    conn.commit()
    cursor.close()

def updata_sqlite_data()->None:
    '''
    下載,並更新資料庫
    '''
    data = __download_youbike_data()
    conn = sqlite3.connect("台北市youbike.db")    
    __create_table(conn)
    for item in data:
        __insert_data(conn,[item['sna'],item['sarea'],item['mday'],item['ar'],item['tot'],item['sbi'],item['bemp']])
    conn.close()

def lastest_datetime_data()->list[tuple]:
    conn = sqlite3.connect("台北市youbike.db")
    cursor = conn.cursor()
    sql = '''
    SELECT 站點名稱,行政區,更新時間,地址,總車輛數,可借,可還
    -- SELECT *
    FROM 台北市youbike
    WHERE (更新時間,站點名稱) IN (
	    SELECT MAX(更新時間),站點名稱
	    FROM 台北市youbike
	    GROUP BY 站點名稱
    )
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return rows

def search_sitename(word:str) -> list[tuple]:
    conn = sqlite3.connect("台北市youbike.db")
    cursor = conn.cursor()
    sql = '''
        -- SELECT id,站點名稱,行政區,MAX(更新時間) AS 更新時間,地址,總車輛數,可借,可還
        -- 改成無id欄位
        SELECT 站點名稱,行政區,MAX(更新時間) AS 更新時間,地址,總車輛數,可借,可還
        FROM 台北市youbike
        GROUP BY 站點名稱
        HAVING 站點名稱 like ?
        '''
    cursor.execute(sql,[f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows