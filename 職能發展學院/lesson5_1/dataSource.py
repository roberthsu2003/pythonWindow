from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.set_window_position(x=-10000, y=-10000)
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
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source,'html.parser')
    driver.close()
    # driver.quit()
    title = soup.find(id=stock_number+"_n",class_="title").string
    t_odd = soup.find(id=stock_number+"_t_odd", class_="oddObj").string
    odd = soup.find(id=stock_number+"_z_odd", class_="oddObj").string
    diff_odd = soup.find(id=stock_number + "_diff_odd").string
    percent_diff = soup.find(id=stock_number + "_pre_odd").string
    return title,t_odd,odd,diff_odd,percent_diff

