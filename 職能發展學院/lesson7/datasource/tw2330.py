
def downloadHTML(code):
    '''
    下載資料，如果成功, 傳出html所有文字
    下載失敗傳出None
    '''
    import requests
    url = f'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID={code}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        response.encoding = "utf-8"
        return response.text
    else:
        return None

def parseHTML(htmlCode):
    '''
    使用BeautifulSoup解析html
    解析表格id = txtFinDetailData內的資料
    取出每個td內的資料
    傳出巢狀list
    '''
    from bs4 import BeautifulSoup
    bs = BeautifulSoup(htmlCode,'html.parser')

    dataList = bs.find('div', attrs={'id': 'txtFinDetailData'}).find_all('tr', attrs={'align': 'center'})
    allDataList = []
    for trTag in dataList:
        tdList = trTag.find_all('td')
        list1 = [tdTag.string for tdTag in tdList]  # comprehension
        allDataList.append(list1)
    return allDataList


def getStackData(stackCode):
        htmlCode = downloadHTML(stackCode)
        if htmlCode is None:
            print("下載失敗")
            return None

        allDataList = parseHTML(htmlCode)
        return allDataList






