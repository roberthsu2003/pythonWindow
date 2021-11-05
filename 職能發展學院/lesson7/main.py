from datasource import getStackData

if __name__ == "__main__":
    print("主執行檔")
    name,allDataList = getStackData(2303)
    print(name)
    print(allDataList)