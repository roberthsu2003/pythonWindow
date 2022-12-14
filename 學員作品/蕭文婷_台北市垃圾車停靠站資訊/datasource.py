import requests
import  json, ssl, urllib.request
import xml.etree.ElementTree as ET  # for parsing XML



#抓高鐵ＡＰＩ車站資訊
def Get_THSRstation():
    # API抓 參考網址 https://tdx.transportdata.tw/api-service/swagger/basic/268fc230-2e04-471b-a728-a726167c1cfc#/THSR/THSRApi_Station_2120
    url = f"https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/Station?%24top=30&%24format=JSON"
    response=requests.get(url=url)
    THSRstation_list=[]  #list

    if response.ok:
        print("下載成功")
        source_data= response.json()["JSON"]
        for item in source_data:
            #建立list資料丟到county_forcase裡
            THSRstation_list.append([item["StationUID"],item["StationID"],item["StationCode"],item["StationName"]["Zh_tw"],item["StationName"]["En"],item["StationAddress"]]) 

        return(THSRstation_list)

    else:
        raise Exception("下載失敗") #自己定義raise 拋出自定義的錯誤訊息




#抓台北市垃圾車資訊
#分隊、地點、局編、抵達時間、經度、緯度、行政區、路線、車次、車號、里別、離開時間
def Get_garbageStation():
    #https://quality.data.gov.tw/dq_download_csv.php?nid=136515&md5_url=4b5e05b9646c77fc75d6d64682554b77
    url=f"https://quality.data.gov.tw/dq_download_json.php?nid=136515&md5_url=4b5e05b9646c77fc75d6d64682554b77"

    #使用SSL module把證書驗證改成不需要驗證即可
    context = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(url, context=context) as jsondata:
            #將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
            data = json.loads(jsondata.read().decode('utf-8-sig')) 
        garbagestation_list=[]  #list
        for i in data:
            garbagestation_list.append(i)
        return garbagestation_list
    except:
        raise Exception("下載失敗") #自己定義raise 拋出自定義的錯誤訊息

#抓台北郵遞區域
def Get_TaipeiArea():
    #寫死
    TaipeiArea = {"全區":"A00",
                  "松山區":"A01",
                   "大安區":"A02",
                   "中正區":"A03",
                   "萬華區":"A05",
                   "大同區":"A09",
                   "中山區":"A10",
                   "文山區":"A11",
                   "南港區":"A13",
                   "內湖區":"A14",
                   "士林區":"A15",
                   "北投區":"A16",
                   "信義區":"A17"
                   }
    return TaipeiArea

#抓台北區域的村里
def Get_AreaVillage(towncode01):
    AreaVillage_list=['全部']  #list
    if towncode01!='A00':
        url=f"https://api.nlsc.gov.tw/other/ListVillage/A/{towncode01}"
        response=requests.get(url=url)
        xml = ET.fromstring(response.content)  # parse XML

    
        for i in xml.iter('villageName'):  
            AreaVillage_list.append(i.text)

    return AreaVillage_list
