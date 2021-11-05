from datasource import getStackData

if __name__ == "__main__":
    print("主執行檔")
    allDataList = getStackData(2317)
    print(allDataList)