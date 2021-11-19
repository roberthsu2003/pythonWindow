__all__ = ["getAirData"]

url = "https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json"

def getAirData():
    '''
    連線空氣品質指標
    :return: None
    '''
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        print("下載成功")
        print(response.text)

