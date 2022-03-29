from models import Spider, UpdateData, GetData
import time
from decimal import Decimal
print(time.gmtime().tm_year - 1)
print(Spider(2330).getPriceNow())
print(GetData().dbFile)
#print(GetData().getListStock())

try:
    z=int("x")
    zz = int("2")
except:
    z=0
    zz = 1
print(z,zz)

x = Spider("2330")
x.getDividendPayment() #取得已發放去年股利公司
#x.getGrossMargin() #取得毛利率
#x.getProfit() #取得利潤資料
'''y = x.getStockInfo() #取得利潤資料
for item in list(y.values()):
    print(item)
    '''
#x.getProfile() #取得基本資料
#x.gerDividend() #取得股利資料
#x.getCompany() #取得上市公司名單
#x.getPrice() #取得收盤價

#Spider().getCompany()
#UpdateData().updateCompanyInfo() #抓取所有上市公司的資料，會執行很久
UpdateData().createDatabase()
#UpdateData().updateProfitAndDividendInfo("2330") #抓取個股營業利潤資料

'''
conn = Data().createConnection()
with conn:
    Data().getStockData(conn, '12330')
    Data().checkCount(conn, '12330')
'''
print(time.gmtime())
print(int("{:0<4}{:0<2}{:0<2}".format(time.gmtime().tm_year,time.gmtime().tm_mon,time.gmtime().tm_mday)))


x = dict()
x["a"] = dict()
x["a"]["a"]=1
if "b" in x:
    print(x , x["b"])
else:
    print(x, "NULL")