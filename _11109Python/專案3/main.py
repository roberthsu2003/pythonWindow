import datasource
tw_county_names = {"台北":"Taipei",
                   "台中":"Taichung",
                   "基隆":"Keelung",
                   "台南":"Tainan",
                   "高雄":"Kaohsiung",
                   "新北":"New Taipei",
                   "宜蘭":"Yilan",
                   "桃園":"Taoyuan",
                   "嘉義":"Chiayi",
                   "新竹":"Hsinchu",
                   "苗栗":"Miaoli",
                   "南投":"Nantou",
                   "彰化":"Changhua",
                   "雲林":"Yunlin",
                   "屏東":"Pingtung",
                   "花蓮":"Hualien",
                   "台東":"Taitung",
                   "金門":"Kinmen",
                   "澎湖":"Penghu",
                   "連江":"Lienchiang"
                   }

def main():
    print("這裏是main function")
    list_data = datasource.get_forcast_data(tw_county_names["基隆"])
    for item in list_data:
        print(item['dt_txt'])

if __name__ == "__main__":
    print("這裏是程式的執行點")
    main()
