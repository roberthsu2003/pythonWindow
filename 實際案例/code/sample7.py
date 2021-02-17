#!usr/bin/python3.8
import sqlite3

def getDateList():
    conn =sqlite3.connect('IMDb.db')
    print('開啟資料庫成功')
    c = conn.cursor()
    cursor=c.execute("SELECT 時間 from 喜愛影片")
    timeSet = set()
    for row in cursor:
        timeSet.add(row[0])
    conn.close()
    return list(timeSet)

if __name__ == "__main__":
    print(getDateList())
    
