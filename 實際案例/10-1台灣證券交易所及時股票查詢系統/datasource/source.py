# 台灣證券交易所
from selenium import webdriver
from .stockInfo import StockInfo
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/Users/roberthsu2003/Downloads/chromedriver')
driver.set_window_position(-10000,0)
def getData(stock_number):
    stockInfo = StockInfo()
    stockInfo.id = stock_number
    url = "https://mis.twse.com.tw/stock/fibest.jsp?stock=" + stock_number
    #檢查driver的網址是否正確
    if driver.current_url == url:
        driver.refresh()
    else:
        print("第一次執行")
        driver.get(url)

    driver.find_element_by_id("btnChangeToOdd").click()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tableNode = soup.find(id="hor-minimalist-a")
    title = soup.find(id=stock_number + "_n", class_="title").string
    #t_odd = soup.find(id=stock_number + "_t_odd").string
    odd = soup.find(id=stock_number + "_z_odd").string
    diff_odd = soup.find(id=stock_number + "_diff_odd").string
    percent_odd = soup.find(id=stock_number + "_pre_odd").string
    tv_odd = soup.find(id=stock_number + "_tv_odd").string
    v_odd = soup.find(id=stock_number + "_v").string
    o_odd = soup.find(id=stock_number + "_o").string
    h_odd = soup.find(id=stock_number + "_h").string
    l_odd = soup.find(id=stock_number + "_l").string
    '''
    print("股票名稱",title)
    #print("成交時間", t_odd)
    print("成交價", odd)
    print("目前狀況", diff_odd)
    print("漲跌價差(百分比)", percent_odd)
    print("當盤_成交量", tv_odd)
    print("累積_成交量", v_odd)
    print("開盤價", o_odd)
    print("最高", h_odd)
    print("最低", l_odd)
    '''
    stockInfo.name = title
    stockInfo.open = o_odd
    stockInfo.close = odd
    stockInfo.high = h_odd
    stockInfo.low = l_odd
    stockInfo.diff = diff_odd
    stockInfo.percent = percent_odd
    return stockInfo

