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
    :return: None
    '''
    import requests
    from requests.exceptions import HTTPError

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

    saveFile(response.text)
    originJson = response.json() #取得原始資料
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





