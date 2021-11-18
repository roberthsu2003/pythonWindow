import json
import csv
import sys

def readIpData(json_file):
    with open(json_file,'r',encoding='utf-8') as file:
        ipCitys=json.load(file)
    return ipCitys

def readQuery(query_file):
    with open(query_file,'r',encoding='utf-8') as file:
        file.__next__()
        rows = csv.reader(file)
        return [row[0] for row in rows]

def sortIP(IPList):
    length = len(IPList)
    for i in range(length-1):
        for j in range(i+1,length):
            if(IPList[i]['ip']>IPList[j]['ip']):
                temp = IPList[i]
                IPList[i] = IPList[j]
                IPList[j] = temp

    return IPList

def binarySearch(array,IP,start,end):
    while(start <= end):
        mid =(start+end) // 2
        if array[mid]['ip'] == IP:
            isFound = True
            break
        else:
            isFound = False

        if(array[mid]['ip'] > IP):
            end = mid - 1
        else:
            start = mid + 1

    if isFound:
        return array[mid]['city']

    return -1

def writeAns(array,ans_file):
    with open(ans_file, 'w', encoding='utf-8') as file:
        csvWriter = csv.writer(file)
        csvWriter.writerow(['ip','city'])
        for oneRow in array:
            csvWriter.writerow(oneRow)
    print("writed finish")

def test_hw2(raw,query,ans):
    ipList = readIpData(raw)
    query = readQuery(query)
    sortedIP = sortIP(ipList[:40000])
    print(sortedIP)
    result = binarySearch(sortedIP, '0.15.73.183', 0, len(sortedIP))
    response = []
    for q in query:
        r = binarySearch(sortedIP,q, 0, len(sortedIP))
        response.append([q,r])
    print(result)
    print(response)
    writeAns(response,ans)


if __name__ == "__main__":
    test_hw2(sys.argv[1],sys.argv[2],sys.argv[3])