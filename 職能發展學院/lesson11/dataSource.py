__all__ = ["getAirData"]

url = "https://data.epa.gov.tw/api/v/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json"

def getAirData():
    '''
    連線行政院環保署空氣品質指標
    有自已的apiKey
    :return: None
    '''
    import requests
    from requests.exceptions import HTTPError
    try:
        response = requests.get(url)
        response.raise_for_status()
    except ConnectionError as e:
        print("連線錯誤",e)
        return None
    except HTTPError as e:
        print("HTTP錯誤", e)
        return None
    except requests.Timeout:
        print("TimeOut")
        return None
    except:
        print("其它錯誤")
        return None
    else:
        print(response.text)
        return "資料"



