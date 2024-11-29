from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# 初始化 Selenium 驅動
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 打開目標網站
    driver.get("https://www.pet.gov.tw/Web/O302.aspx")
    driver.maximize_window()

    # 等待表格加載完成，改用更靈活的等待條件
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table"))
    )

    # 提取網頁 HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 提取表格數據
    table = soup.find('table', {'class': 'table'})
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    rows = table.find('tbody').find_all('tr')

    data = []
    for row in rows:
        cols = [td.text.strip() for td in row.find_all('td')]
        data.append(dict(zip(headers, cols)))

    # 輸出數據
    for record in data:
        print(record)

        # 將資料存儲為 JSON 文件（可選）
    import json
    with open('pet_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

finally:
    # 關閉瀏覽器
    driver.quit()
