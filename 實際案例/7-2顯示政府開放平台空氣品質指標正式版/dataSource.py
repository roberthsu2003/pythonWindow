__all__ = ["getAirData"]


class CityWeather():
    def __init__(self,siteName=None,county=None,aqi=None,pm25=None,status=None,time=None):
        self.siteName = siteName
        self.county = county
        self.aqi = aqi
        self.pm25 = pm25
        self.status = status
        self.time = time


def getAirData():
    '''
    連線行政院環保署空氣品質指標
    有自已的apiKey
    :return: 傳出citys,list內有自訂實體CityWeather
    '''
    import requests
    from requests.exceptions import HTTPError
    import json

    url = "https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except ConnectionError as e:
        raise ValueError("連線錯誤")
    except HTTPError as e:
        raise ValueError("HTTP錯誤")
    except requests.Timeout:
        raise ValueError("TimeOut")
    except:
        raise ValueError("其它錯誤")

    saveFile(response.text) #儲存檔案
    jsonFilePath = getlastestFilePath() #取得最新儲存檔案的路徑

    #開啟json檔
    jsonFile = open(jsonFilePath,'r',encoding="utf-8")
    originJson = json.load(jsonFile) #解析json的file物件，成為python的基本資料結構
    jsonFile.close()
    #originJson = response.json() #取得原始資料
    records = originJson["records"]

    #解析資料

    cities = [CityWeather(siteName=dict["SiteName"],county=dict["County"],aqi=dict["AQI"],pm25=dict["PM2.5"],status=dict["Status"],time=dict["ImportDate"]) for dict in records]

    return cities

def saveFile(fileContent):
    '''
    :param fileContent: 要儲存的文字內容
    :return: None
    '''
    import os
    from datetime import datetime
    folderName = "data" #資料夾名稱
    now = datetime.now()
    fileName = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.json" #存檔的檔案名稱
    savePath = f"./{folderName}/{fileName}"
    absPath = os.path.abspath(savePath) #存檔的絕對路徑

    #檢查有沒有資料夾, 沒有就建立資料夾
    if not os.path.exists(folderName):
        os.mkdir(folderName)

    #儲存檔案
    file = open(absPath,"wt",encoding="utf-8")
    file.write(fileContent)
    file.close()
    print("存檔完畢")

def getlastestFilePath():
    '''
    取得data資料夾內最新的檔案
    :return:傳出最新json檔的絕對路徑
    '''
    import os
    from datetime import datetime
    folderName = "data"

    fileNames = os.listdir(folderName)  #取得data資料夾內檔案名稱的list
    datetimeList = [datetime.strptime(fileName,"%Y-%m-%d-%H-%M-%S.json") for fileName in fileNames] #建立list,裏面是datatime物件
    datetimeList.sort(reverse=True) #排序datatimes物件，由大到小
    lestestDateTime = datetimeList[0] #取出最新的dateTime物件
    #透過datatime物件建立檔案名稱
    fileName = f"{lestestDateTime.year}-{lestestDateTime.month}-{lestestDateTime.day}-{lestestDateTime.hour}-{lestestDateTime.minute}-{lestestDateTime.second}.json"
    absFileName=os.path.abspath(f"{folderName}/{fileName}") #取出最新檔案的絕對路徑
    return absFileName






