# data.py 就是自訂的 module
# 全球COVID-19累積病例數與死亡數 的 csv檔, 線上下載
from .Covid19Info import Covid19Info

FILENAME = '../covid19.csv'
covid19Data = None

def downloadCovid19DataFromPlatForm():
    '''
    從政府開放平台下載疾管署全球Covid19的資料，每1日，政府會更新一次
    '''
    import requests
    downloadURL = "https://od.cdc.gov.tw/eic/covid19/covid19_global_cases_and_deaths.csv"
    response = requests.get(downloadURL, stream=True)
    response.encoding = 'utf-8'
    # 檢查是否下載正常
    if response.status_code != 200:
        return

    with open(FILENAME, 'wb') as fileObj:
        # 寫入檔案
        for chunk in response.iter_content(chunk_size=128):
            # print('chunk =', chunk)
            fileObj.write(chunk)

def readAndParseCSVFile():
    '''
    解析下載完成的 covid19.csv.
    傳出 python 的資料結構
    傳出list,list內的元素是Covid19Info實體
    '''
    import csv
    global covid19Data
    # 解析 covid19.CSV
    with open(FILENAME, newline='', encoding='utf-8') as csvfile:
        next(csvfile)  # 跳過第一行首標題列
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        # 以迴圈輸出每一列
        covid19Lst = []
        seqno = 0
        for row in rows:
            seqno += 1
            item = Covid19Info()
            item.seq = seqno
            item.country_ch = row[0]
            item.country_en = row[1]
            item.cases = row[2]
            item.deaths = row[3]
            covid19Lst.append(item)
        covid19Data = covid19Lst


def getCovid19Data():
    downloadCovid19DataFromPlatForm()  # 下載檔案
    readAndParseCSVFile()
    return covid19Data




