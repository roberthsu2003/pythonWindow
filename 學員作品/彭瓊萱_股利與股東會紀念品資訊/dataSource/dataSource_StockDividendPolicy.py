# dataSource_StockDividendPolicy.py
# 資料來源：GoodInfo 台灣股市資訊網
# 查詢股利政策資訊

import requests
from requests import ConnectionError, HTTPError, Timeout
import sqlite3
from sqlite3 import Error as sqlite3Error
from bs4 import BeautifulSoup
import re

databaseName = 'dataSource/StockInfo.db'


__all__ = ['download_save_to_DataBase', 'get_stock_info', 'get_dividend']


def download_stock_dividend_policy_data(stockId):
    # id = 1101
    # url = f'https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={stockId}'
    url = f'https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={stockId}'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        response.raise_for_status()
    except ConnectionError as e:
        print("網路連線有問題")
        print(e)
        return
    except HTTPError as e:
        print("網路連線有問題")
        print(e)
        return
    except Timeout as e:
        print("網路連線有問題")
        print(e)
        return
    except:
        print("網路連線有問題")
        return
    return response.text

def get_id_name_data(soupDatas):
    idNameList = ['','']
    tempIdNameDivTableData = soupDatas.find_all("table", class_="b0 p6_0")
    if len(tempIdNameDivTableData) > 0:
        for itemTable in tempIdNameDivTableData:
            tempRowTags = itemTable.find_all("tr")
            for itemRow in tempRowTags:
                itemText = itemRow.get_text()
                tempIdNameText = re.search("歷年股利政策一覽表", itemText)
                if tempIdNameText != None:
                    idNameList = itemText.split()
                    return idNameList[:2]
    return idNameList

def convert_htmltag_to_list(dataHtmlTag):
    resultList = []
    soup = BeautifulSoup(dataHtmlTag, 'html.parser')
    datas = soup.find('div', id='divDividendDetailData').find_all('tr', align='center')

    idNameList = get_id_name_data(soup)

    for tr_item in datas[:(len(datas)-1)]:
        tdList = tr_item.find_all('td')
        tdRow = [td_item.get_text() for td_item in tdList]
        tdRow = idNameList+tdRow
        resultList.append(tdRow)

    return resultList


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3Error as e:
        print("sqlite連線錯誤")
        print(e)
    return conn


def create_stock_dividend_policy_table(conn):
    sql = '''
        CREATE TABLE IF NOT EXISTS stock_dividend_policy_data (
            Id TEXT,
            Name TEXT,
            股利發放年度 TEXT,
            現金股利_盈餘 TEXT,
            現金股利_公積 TEXT,
            現金股利_合計 TEXT,
            股票股利_盈餘	TEXT,
            股票股利_公積 TEXT,
            股票股利_合計 TEXT,
            股利合計 TEXT,
            股利總計_現金	TEXT,
            股利總計_股票 TEXT,
            填息花費日數 TEXT,
            填權花費日數 TEXT,
            股價年度  TEXT,
            股價統計_最高  TEXT,
            股價統計_最低  TEXT,
            股價統計_年均  TEXT,
            年均殖利率_現金 TEXT,
            年均殖利率_股票 TEXT,
            年均殖利率_合計 TEXT,
            股利所屬期間 TEXT,
            EPS TEXT,
            盈餘分配率_配息 TEXT,
            盈餘分配率_配股 TEXT,
            盈餘分配率_合計 TEXT,
            資料日期 TEXT,
            PRIMARY KEY(Id, 股利發放年度),
            UNIQUE (Id, 股利發放年度)
        );
        '''
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except sqlite3Error as e:
        print(e)

def replace_stock_dividend_policy_data(conn, stockId, dataList):
    from datetime import datetime
    def get_datadate_string():
        return datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    sql = '''
            INSERT or replace  INTO stock_dividend_policy_data (Id, Name, 股利發放年度, 現金股利_盈餘, 現金股利_公積, 
            現金股利_合計, 股票股利_盈餘, 股票股利_公積, 股票股利_合計, 股利合計, 股利總計_現金, 股利總計_股票, 填息花費日數, 
            填權花費日數, 股價年度, 股價統計_最高, 股價統計_最低, 股價統計_年均, 年均殖利率_現金, 年均殖利率_股票, 年均殖利率_合計, 
            股利所屬期間, EPS, 盈餘分配率_配息, 盈餘分配率_配股, 盈餘分配率_合計, 資料日期)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    try:
        cursor = conn.cursor()

        for item in dataList:
            item.append(get_datadate_string())
            cursor.execute(sql, item)
            conn.commit()
    except sqlite3Error as e:
        print(e)

def download_save_to_DataBase(stockId = '1101'):
    print("download_save_to_DataBase (Stock Dividend) ...")
    htmlTagData = download_stock_dividend_policy_data(stockId)
    if htmlTagData == None:
        return
    dataList = convert_htmltag_to_list(htmlTagData)

    conn = create_connection(databaseName)
    with conn:
        create_stock_dividend_policy_table(conn)
        replace_stock_dividend_policy_data(conn, stockId, dataList)

def get_stock_info(stockId='1101'):
    rows = None
    conn = create_connection(databaseName)
    sql = f'''
        select id,name,"股利發放年度","現金股利_合計","股票股利_合計","股利合計","填息花費日數","股價統計_最高","股價統計_最低","股價統計_年均","年均殖利率_合計" 
        from stock_dividend_policy_data
        where Id = '{stockId}' and  Id <> '' and 股利發放年度 <> '∟' 
        order by 股利發放年度 desc
    '''

    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except sqlite3Error as e:
            print(e)
    return rows

def get_dividend(stockId='1101'):
    result = None
    conn = create_connection(databaseName )
    sql = f'''
    select 股利合計 from stock_dividend_policy_data 
    where Id = '{stockId}' and  Id <> '' and 股利發放年度 <> '∟' and 股利合計 <> '-' 
    order by 股利發放年度 DESC limit 1
    '''
    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                result = row[0]
        except sqlite3Error as e:
            print(e)
    return result
