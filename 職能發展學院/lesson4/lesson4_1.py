#!/usr/bin/python3.10
import requests

urlpath = '	https://data.epa.gov.tw/api/v1/aqx_p_02?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&sort=ImportDate%20desc&format=json'
def downloadData():
    response = requests.get(urlpath)
    if response.status_code == 200:
        print('下載成功')
        data = response.json()
        print(data)

def main():
    downloadData()

if __name__ == '__main__':
    main()