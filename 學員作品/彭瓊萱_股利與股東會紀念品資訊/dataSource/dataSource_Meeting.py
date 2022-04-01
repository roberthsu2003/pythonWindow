# 查詢股東會紀念品
# 資料來源：Hi Stock 嗨投資
# https://histock.tw/stock/gift.aspx

import requests
from requests import ConnectionError, HTTPError, Timeout
import sqlite3
from sqlite3 import Error as sqlite3Error
from bs4 import BeautifulSoup
import re

databaseName = 'dataSource/StockInfo.db'
__all__ = ['download_save_to_DataBase', 'get_meeting_info', 'get_meetings_of_oneyear_info']

def download_meeting_data():
    # url = f'https://histock.tw/stock/gift.aspx'
    url = f'https://histock.tw/stock/gift.aspx'

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


def convert_htmltag_to_list(dataHtmlTag):
    resultList = []
    soup = BeautifulSoup(dataHtmlTag, 'html.parser')
    dataMainDiv = soup.find("div", class_="grid pt10")

    h3_title_tag = dataMainDiv.find("h3", class_="seoh3")
    if h3_title_tag != None:
        meeting_year_text = h3_title_tag.get_text()
        meeting_year = re.findall("^\d+", meeting_year_text)
        if len(meeting_year) > 0:
            meeting_year = meeting_year[0]  # 股東會年度
    datas = dataMainDiv.find_all("div", class_="grid-body")

    for dataItem in datas:
        h5_tags = dataItem.find_all("h5")
        for h5_tag in h5_tags:
            h5_item_text = h5_tag.get_text()
            if re.search("最新公告", h5_item_text) != None:
                tempDateText = h5_item_text.split()
                if len(tempDateText) > 0:
                    dataDate = tempDateText[0]  # 資料日期

            elif re.search("最後買進日未到期", h5_item_text) != None:
                tempYearText = re.search("\d+", h5_item_text)
                if tempYearText != None:
                    dataYear = tempYearText.group(0)    # 資料年度
                dataNotExpiredTag = h5_tag.find_next("table", class_="gvTB")

            elif re.search("最後買進日已到期", h5_item_text) != None:
                dataExpiredTag = h5_tag.find_next("table", class_="gvTB")

    # 最後買進日未到期
    for tr_item in dataNotExpiredTag.find_all("tr"):
        td_item_tag = tr_item.find_all("td")
        if len(td_item_tag) > 0:
            trRow = [str(dataYear)]
            for item in td_item_tag:
                newItem = item.get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace("\xa0參考圖", "")
                trRow.append(newItem)
            if len(trRow) > 0:
                trRow.pop(-1)
            trRow.append('未到期')
            resultList.append(trRow)

    # 最後買進日已到期
    for tr_item in dataExpiredTag.find_all("tr"):
        td_item_tag = tr_item.find_all("td")
        if len(td_item_tag) > 0:
            trRow = [str(dataYear)]
            for item in td_item_tag:
                newItem = item.get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace("\xa0參考圖", "")
                trRow.append(newItem)
            if len(trRow) > 0:
                trRow.pop(-1)
            trRow.append('已到期')
            resultList.append(trRow)
    if resultList[0] == []:
        resultList.pop(0)
    return resultList


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3Error as e:
        print("sqlite連線錯誤")
        print(e)
        return
    return conn


def create_meetings_table(conn):
    sql = '''
        CREATE TABLE IF NOT EXISTS meetings_data (
            stock_YER TEXT,
            stock_Id TEXT,
            stock_Name TEXT,
            股價 TEXT,
            最後買進日 TEXT,
            股東會日期 TEXT,
            性質 TEXT,
            開會地點	TEXT,
            股東會紀念品 TEXT,
            零股寄單 TEXT,
            股代 TEXT,
            股代電話	TEXT,
            是否到期 TEXT,
            PRIMARY KEY(stock_YER, stock_Id),
            UNIQUE (stock_YER, stock_Id)
        );
        '''
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        print("create table (meetings_data)...")
    except sqlite3Error as e:
        print(e)

def replace_meetings_data(conn, dataList):
    sql = '''
            INSERT or replace  INTO meetings_data (stock_YER, stock_Id, stock_Name, 股價, 最後買進日, 股東會日期, 性質, 開會地點, 股東會紀念品,
                零股寄單, 股代, 股代電話, 是否到期)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    try:
        cursor = conn.cursor()

        for item in dataList:
            cursor.execute(sql, (item))
            conn.commit()
    except sqlite3Error as e:
        print(e)


def download_save_to_DataBase():
    print("download_save_to_DataBase(Meeting) ...")
    htmlTagData = download_meeting_data()
    if htmlTagData == None:
        return

    dataList = convert_htmltag_to_list(htmlTagData)

    conn = create_connection(databaseName)
    with conn:
        create_meetings_table(conn)
        replace_meetings_data(conn, dataList)

def get_meeting_info(stockId='1101'):
    rows = None
    conn = create_connection(databaseName)
    sql = f'''
        select stock_YER, stock_Id, stock_Name, 股價, 最後買進日, 股東會日期, 性質, 開會地點, 股東會紀念品,  零股寄單, 股代, 股代電話, 是否到期 
        from "meetings_data"
        where stock_Id = '{stockId}'
        order by stock_YER DESC, 是否到期 desc, stock_Id
    '''

    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except sqlite3Error as e:
            print(e)
    return rows

def get_meetings_of_oneyear_info(m_year='2022', m_type=0):
    rows = None
    queryType = ""
    if m_type == 1:
        queryType = " and 是否到期 = '未到期'"
    elif m_type == 2:
        queryType = " and 是否到期 = '已到期'"

    conn = create_connection(databaseName)
    sql = f'''
        select stock_YER, stock_Id, stock_Name, 股價, 最後買進日, 股東會日期, 性質, 開會地點, 股東會紀念品,  零股寄單, 股代, 股代電話, 是否到期 
        from "meetings_data"
        where stock_YER = '{m_year}'
        {queryType}
        order by stock_YER DESC, 是否到期 desc, stock_Id
    '''

    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except sqlite3Error as e:
            print(e)
    return rows