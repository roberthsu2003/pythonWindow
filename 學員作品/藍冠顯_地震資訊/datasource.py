import requests


def get_report_data(api_key):
    url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={api_key}&format=JSON&areaName="

    response = requests.get(url=url)
    earthquake_list = []
    earthquake_list2 = []
    if response.ok:
        print("下載成功")

        data_number = len(response.json()["records"]["earthquake"])

        data_source = response.json(
        )["records"]["earthquake"]

        for i in range(data_number):
            earthquake_list.append(data_source[i])

        for item in earthquake_list:
            earthquake_list2.append(
                [item["reportContent"], item["web"], item["reportImageURI"]])

        return (earthquake_list2)

    else:
        raise Exception(f"下載失敗")
