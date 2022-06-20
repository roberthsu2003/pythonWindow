from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def getData(stock_number):
    url = "https://mis.twse.com.tw/stock/fibest.jsp?stock=" + stock_number
    if driver.current_url == url:
        driver.refresh()
    else:
        driver.get(url)


if __name__ == "__main__":
    getData("2330")



