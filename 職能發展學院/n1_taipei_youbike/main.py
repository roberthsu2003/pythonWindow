import requests

def get_youbike_data():
    url = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json'
    response = requests.get(url)
    allData = response.json()
    youbikeData = list(allData['retVal'].values())
    return youbikeData



if __name__ == "__main__":
    youbikeData = get_youbike_data()
    for siteInfo in youbikeData:
        print(siteInfo['sna'])
        print('可借:', siteInfo['sbi'])
        print('可還:', siteInfo['bemp'])
        print('========================')