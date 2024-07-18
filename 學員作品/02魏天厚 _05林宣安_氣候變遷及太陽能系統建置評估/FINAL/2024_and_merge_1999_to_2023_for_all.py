import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 初始化啟動chrome webdriver
driverpath = os.path.join('chromedriver.exe')
service = Service(driverpath)

# 設置Chrome選項以啟用無頭模式
options = Options()
options.add_argument('--headless')  # 啟用無頭模式
options.add_argument('--disable-gpu')  # 如果你使用的是Windows系統，這一步是必要的
options.add_argument('--no-sandbox')  # 對於Linux系統可能是必要的
options.add_argument('--disable-dev-shm-usage')  # 共享內存設置

browser = webdriver.Chrome(service=service, options=options)  # 模擬瀏覽器
wait = WebDriverWait(browser, 10)  # 設置顯式等待時間

url = 'https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html'
browser.get(url)  # 以get方式進入網站
time.sleep(3)  # 網站有loading時間

# 找出年份和月份的選單定位
year_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Year"]')))  # 使用XPath定位年份選單
month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Month"]')))  # 使用XPath定位月份選單

# 打開年份選單並選擇2024年
year_dropdown.click()
time.sleep(1)  # 確保下拉選單打開
year_option = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Year"]/option[text()="2024"]')))
year_option.click()

# 初始化存儲2024年數據的列表
yearly_data = []

# 遍歷2024年的12個月
for month in range(1, 13):
    # 打開月份選單並選擇對應月份
    month_dropdown.click()
    time.sleep(1)  # 確保下拉選單打開

    # 檢查月份選項是否存在
    try:
        month_option = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="Month"]/option[text()="{month}"]')))
        month_option.click()
    except:
        print(f"2024年{month}月的數據不可用，跳過")
        continue

    # 顯式等待表格加載完成
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        time.sleep(3)  # 追加等待時間確保數據完全加載
    except:
        print(f"2024年{month}月的數據表格未加載，跳過")
        continue

    # 使用pandas讀取HTML表格
    try:
        tables = pd.read_html(browser.page_source)
        df = tables[0]
    except ValueError:
        print(f"2024年{month}月的表格數據讀取失敗，跳過")
        continue

    # 添加年份和月份列
    df['Year'] = 2024
    df['Month'] = month

    # 將數據添加到年度列表中
    yearly_data.append(df)

# 關閉瀏覽器
browser.quit()

# 合併2024年的數據
if yearly_data:
    yearly_df = pd.concat(yearly_data, ignore_index=True)

    # 打印2024年抓取到的數據
    print("2024年的數據：")
    print(yearly_df)

    # 保存2024年的數據為CSV
    yearly_df.to_csv('data_2024.csv', index=False, encoding='utf-8-sig')

    # 保存2024年的數據為JSON
    yearly_df.to_json('data_2024.json', orient='records', force_ascii=False)

print("2024年的數據已保存為CSV和JSON格式")

# 合併1999-2023年和2024年的數據
try:
    previous_data = pd.read_csv('data_1999_to_2023.csv', encoding='utf-8-sig')
    combined_data = pd.concat([previous_data, yearly_df], ignore_index=True)

    # 保存合併後的數據為CSV
    combined_data.to_csv('data_1999_to_2024.csv', index=False, encoding='utf-8-sig')

    # 保存合併後的數據為JSON
    combined_data.to_json('data_1999_to_2024.json', orient='records', force_ascii=False)

    print("1999年至2024年的數據已保存為CSV和JSON格式")
except FileNotFoundError:
    print("找不到1999年至2023年的數據文件，請確保該文件存在")

