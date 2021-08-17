import requests
import xml.etree.cElementTree as ET #used to analyse xml
import re #used to fetch numbers


class GetInfo:
    def __init__(self):
        self.itemList = []


    def getInfoFromWeb(self):
        '''
        get all invoice lottery xml from the website
        return: all available information from xml into a list
        '''
        content = requests.get("https://invoice.etax.nat.gov.tw/invoice.xml")
        tree = ET.fromstring(content.text)
        self.itemList = list(tree.iter(tag="item"))
        return self.itemList

    def DataTransform(self, itemList):
        '''
        transform the web data into a simple list
        :param itemList: the return itemlist from getInfoFromWeb()
        :return: the list of latest 3 invoice lotteries including Months, numbers, date
        '''
        self.itemList = itemList
        monthPrice = []
        for i in range(3):
            monthPrice.append([])
            priceMonth = self.itemList[i][0].text
            priceNumbers = self.itemList[i][2].text
            getPriceNumbers = re.findall(r"\d{3,8}", priceNumbers) #get numbers with 3 and 8 digits
            openDate = self.itemList[i][3].text
            priceMonth = priceMonth + "月"
            openDate = openDate[:10]
            monthPrice[i].append(priceMonth)
            monthPrice[i].append(getPriceNumbers)
            monthPrice[i].append(openDate)
        return monthPrice



