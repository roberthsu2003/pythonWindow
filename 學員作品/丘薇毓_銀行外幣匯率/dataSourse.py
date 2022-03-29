import sqlite3
from sqlite3 import Error as sqlite3Error
import download_all

databaseName = 'rate.db'

# 提供給外部的 def
__all__ = ['create_connection','create_table_rate','saveToDataBase','get_bank_name','get_coin_info','get_usd','get_eur','get_jpy','get_cny','get_aud','get_gbp','get_sgd','get_krw','get_zar']

def create_connection(db_file):
    '''
    連線至資料庫
    :param db_file: 資料庫的檔案名稱
    :return: Connection物件
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3Error as e:
        print('sqlite連線錯誤')
        print(e)
        return
    return conn

def create_table_rate(conn):
    sql='''
    CREATE TABLE IF NOT EXISTS rate(
    bank TEXT ,
    coinTW TEXT,
    coin TEXT NOT NULL,
    nowbuy TEXT,
    nowsale TEXT,
    cashbuy TEXT,
    cashsale TEXT,
    UNIQUE(bank,coin)
    );
    '''
    cursor = conn.cursor()
    try:
        cursor.execute(sql) #執行
    except sqlite3Error as e:
        print(e)


def saveToDataBase():
    conn = create_connection(databaseName)
    create_table_rate(conn)
    cathay = download_all.download_cathay()
    land = download_all.download_land()
    taiwan = download_all.download_taiwan()
    citi = download_all.download_citi()
    esun = download_all.download_esun()
    with conn:
        replace_cathay(conn, cathay)
        replace_land(conn, land)
        replace_taiwan(conn,taiwan)
        replace_citi(conn,citi)
        replace_esun(conn,esun)

# ----get data

def get_bank_name():
    conn = create_connection(databaseName)
    sql ='''
        SELECT DISTINCT bank
        FROM rate
        '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        bank_name_list = [row[0] for row in rows]
        return bank_name_list

def get_coin_info(bank):
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE bank=?
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql,(bank,))
        rows = cursor.fetchall() #返回多個的元組
        return rows


def get_usd():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'USD'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        # rows = cursor.fetchone() #返回單個的元組
        return rows

def get_eur():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'EUR'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        # rows = cursor.fetchone() #返回單個的元組
        return rows

def get_jpy():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'JPY'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        # rows = cursor.fetchone() #返回單個的元組
        return rows

def get_cny():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'CNY'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        return rows

def get_aud():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'AUD'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        return rows

def get_gbp():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'GBP'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        return rows

def get_sgd():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'SGD'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        return rows

def get_krw():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'KRW'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        return rows

def get_zar():
    conn = create_connection(databaseName)

    sql ='''
        SELECT *
        FROM rate
        WHERE coin = 'ZAR'
        '''

    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall() #返回多個的元組
        return rows


# 內部更新資料---------------------
def replace_cathay(conn,dataList):
    sql='''
    INSERT or replace INTO 
    rate(bank,coinTW,coin,nowbuy,nowsale,cashbuy,cashsale)
    VALUES('國泰銀行',?,?,?,?,?,?)
    '''
    try:
        cursor = conn.cursor()
        for item in dataList:
            coinTW = item[0].split('(', 1)[0].split(')', 1)[0]
            coin = item[0].split('(',1)[1].split(')',1)[0]
            nowbuy = item[1]
            nowsale = item[2]
            cashbuy = item[3]
            cashsale = item[4]
            cursor.execute(sql, (coinTW,coin, nowbuy, nowsale, cashbuy, cashsale))
        print('cathay輸入完成')
    except sqlite3Error as e:
        print(e)
    conn.commit()

def replace_land(conn,dataList):
    sql='''
    INSERT or replace INTO 
    rate(bank,coinTW,coin,nowbuy,nowsale,cashbuy,cashsale)
    VALUES('土地銀行',?,?,?,?,?,?)
    '''
    try:
        cursor = conn.cursor()
        for item in dataList:
            coinTW = item[0].split('(',1)[0].split(')',1)[0]
            coin = item[0].split('(',1)[1].split(')',1)[0]
            nowbuy = item[1]
            nowsale = item[2]
            cashbuy = item[3]
            cashsale = item[4]
            cursor.execute(sql, (coinTW,coin, nowbuy, nowsale, cashbuy, cashsale))
        print('land輸入完成')
    except sqlite3Error as e:
        print(e)
    conn.commit()

def replace_taiwan(conn,dataList):
    sql='''
    INSERT or replace INTO 
    rate(bank,coinTW,coin,nowbuy,nowsale,cashbuy,cashsale)
    VALUES('臺灣銀行',?,?,?,?,?,?)
    '''
    try:
        cursor = conn.cursor()
        for item in dataList:
            coinTW = item[0].split('(',1)[0].split(')',1)[0]
            coin = item[0].split('(',1)[1].split(')',1)[0]
            nowbuy = item[3]
            nowsale = item[4]
            cashbuy = item[1]
            cashsale = item[2]
            cursor.execute(sql, (coinTW,coin, nowbuy, nowsale, cashbuy, cashsale))
        print('taiwan輸入完成')
    except sqlite3Error as e:
        print(e)
    conn.commit()

def replace_citi(conn,dataList):
    sql='''
    INSERT or replace INTO 
    rate(bank,coinTW,coin,nowbuy,nowsale,cashbuy,cashsale)
    VALUES('花旗銀行',?,?,?,?,?,?)
    '''
    try:
        cursor = conn.cursor()
        for item in dataList:
            coinTW = item[0]
            coin = item[1]
            nowbuy = item[3]
            nowsale = item[2]
            cashbuy = item[5]
            cashsale = item[4]
            cursor.execute(sql, (coinTW,coin, nowbuy, nowsale, cashbuy, cashsale))
        print('citi輸入完成')
    except sqlite3Error as e:
        print(e)
    conn.commit()

def replace_esun(conn,dataList):
    sql='''
    INSERT or replace INTO 
    rate(bank,coinTW,coin,nowbuy,nowsale,cashbuy,cashsale)
    VALUES('玉山銀行',?,?,?,?,?,?)
    '''
    try:
        cursor = conn.cursor()
        for item in dataList:
            coinTW = item[0].split('(',1)[0].split(')',1)[0]
            coin = item[0].split('(',1)[1].split(')',1)[0]
            nowbuy = item[1]
            nowsale = item[2]
            cashbuy = item[3]
            cashsale = item[4]
            cursor.execute(sql, (coinTW,coin, nowbuy, nowsale, cashbuy, cashsale))
        print('esun輸入完成')
    except sqlite3Error as e:
        print(e)
    conn.commit()

# ====