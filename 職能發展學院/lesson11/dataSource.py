__all__ = ["getAirData"]



def getAirData():
    '''
    連線行政院環保署空氣品質指標
    有自已的apiKey
    :return: None
    '''
    import requests
    from requests.exceptions import HTTPError

    url = "https://data.epa.gov.tw/api/v/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json"

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
    else:
        print(response.text)
        return "資料"



