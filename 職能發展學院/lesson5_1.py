from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def getData(stock_number):
    url = "https://mis.twse.com.tw/stock/fibest.jsp?stock=" + stock_number
    try:
        if driver.current_url == url:
            driver.refresh()
        else:
            driver.get(url)
    except Exception as e:
        print(f"伺服器發生錯誤:{e}")

    driver.find_element(By.ID,"btnChangeToOdd").click()
    soup = BeautifulSoup(driver.page_source,'html.parser')
    title = soup.find(id=stock_number+"_n",class_="title").string
    print(title)


if __name__ == "__main__":
    getData("2330")



