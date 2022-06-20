from selenium import webdriver
import time
driver=webdriver.Chrome('./chromedriver')
driver.get("https://www.google.com.tw")
time.sleep(3)
driver.close()


