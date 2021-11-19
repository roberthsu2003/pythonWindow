__all__ = ["getAirData"]

url = "https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json"

def getAirData():
    '''
    連線空氣品質指標
    :return: None
    '''
    import requests
    from  requests.exceptions import HTTPError
    try:
        response = requests.get(url)
        response.raise_for_status()
    except ConnectionError as e:
        print("連線錯誤",e)
        return
    except HTTPError as e:
        print("HTTP錯誤", e)
        return
    except requests.Timeout:
        print("TimeOut")
        return
    except:
        print("其它錯誤")
        return
    else:
        print("下載成功")
        print(response.text)



