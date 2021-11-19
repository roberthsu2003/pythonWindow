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

    originJson = response.json() #取得原始資料
    records = originJson["records"]

    #解析資料

    cities = [CityWeather(siteName=dict["SiteName"],county=dict["County"],aqi=dict["AQI"],pm25=dict["PM2.5"],status=dict["Status"],time=dict["ImportDate"]) for dict in records]

    return cities



