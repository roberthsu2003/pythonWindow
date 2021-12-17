#必需先安裝2個套件
#selenium4.0以上不需要手動下載webdriver軟體，只需要安裝2個套件
#pip install selenium
#pip3install webdriver_manager

#selenium4.0以上初始化webdriver的方式
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

__all__ = ["getStockInfo"]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  #初始化webdriver

class StockInfo():
    def __init__(self):
        self.title = None

def getStockInfo(odd_number):
    """
    收集台灣證券交易所的資料,一次只收集一支股票的及時資料
    :param odd_number: 股票的編號:string
    :return: StockInfo的實體
    """
    #建立一個收集資料內容的StockInfo實體
    stackInfo = StockInfo()
    #連結網址
    url = f"https://mis.twse.com.tw/stock/fibest.jsp?stock={odd_number}"

    # 舊版
    # driver = webdriver.Chrome(r"C:\Users\User\Downloads\chromedriver_win32\chromedriver")
    driver.get(url)

    # 等待一段時間
    time.sleep(2)
    # 等網頁DOM下載完後，最多等待5秒
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, f'{odd_number}_z')))

    # driver.find_element(By.ID,'btnChangeToOdd').click() #模擬使用者按這個按鈕
    webPageText = driver.page_source
    # print(webPageText)
    soup = BeautifulSoup(webPageText, 'html.parser')
    # title
    # <label id="2330_n" class="title">[上市]  2330  台積電</label>

    title = soup.find('label', {'id': f'{odd_number}_n', 'class': 'title'}).string

    # title = soup.find(id=f'{odd_number}_n,class_=title).string #另一種寫法
    stackInfo.title = title

    # <td width="6%" class="oddObj" id="2330_v" align="center">23001</td>
    # 累紀成交量
    total_odd = soup.find('td', {'id': f'{odd_number}_v', 'class': 'oddObj'}).string
    print(f'累積成交量:{total_odd}')

    # 開盤價
    # <td width="6%" class="oddObj" id="2330_o" align="center" style="">614.00</td>

    openPrice = soup.find('td', {'id': f'{odd_number}_o', 'class': 'oddObj'}).string
    print(f"開盤價:{openPrice}")

    # 當日最高
    # <td width="6%" class="oddObj" id="2330_h" align="center">614.00</td>

    hightest = soup.find('td', {'id': f'{odd_number}_h', 'class': 'oddObj'}).string
    print(f"當日最高:{hightest}")

    # 當日最低
    # <td width="6%" class="oddObj" id="2330_l" align="center">606.00</td>

    lowest = soup.find('td', {'id': f'{odd_number}_l', 'class': 'oddObj'}).string
    print(f"當日最低:{lowest}")

    # 撮合時間
    # <td id="2330_t" align="center">13:30:00</td>

    mathTime = soup.find('td', {'id': f'{odd_number}_t'}).string
    print(f"撮合時間:{mathTime}")

    # 成交價
    # <td id="2330_z" align="center" style="color: rgb(16, 80, 16);">608.00</td>

    rightPrice = soup.find('td', {'id': f'{odd_number}_z'}).string
    print(f"成交價:{rightPrice}")

    # 漲跌價差(百分比)
    # <td align="center">
    # <label id="2330_diff" style="color: rgb(16, 80, 16);">▼-7.00</label>
    # <label id="2330_pre" style="color: rgb(16, 80, 16);">(-1.14%)</label>
    # </td>

    differentPrice = soup.find('label', {'id': f'{odd_number}_diff'}).string
    print(f"漲跌價差:{differentPrice}")

    differentPercent = soup.find('label', {'id': f'{odd_number}_pre'}).string
    print(f"漲跌(百分比):{differentPercent}")

    # 成交量
    # <td id="2330_tv" align="center">4610</td>

    dealCount = soup.find('td', {'id': f'{odd_number}_tv'}).string
    print(f"成交量:{dealCount}")
    driver.close()
    return stackInfo