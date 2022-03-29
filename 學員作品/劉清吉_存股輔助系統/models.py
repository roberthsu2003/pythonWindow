import requests
from bs4 import BeautifulSoup
import urllib.request, csv, sqlite3, time
from sqlite3 import Error as sqlite3Error
from decimal import Decimal

__all__ = ['Spider().getPriceNow()','GetData().getListDividend()','GetData().getListStock()','GetData().getSumInfo()']

class Spider:
    def __init__(self, id: str = None):
        self.id = id
        self.listProfile = dict()
        self.listDividend = dict()
        self.listProfit = dict()
        self.listCompany = dict()
        self.listDividendPayment = list()

    def headersUpdate(self):
        """headers = requests.utils.default_headers()

        headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )
        headers.update = {
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}"""
        from random import randint

        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",

        ]
        random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
        headers = {'User-Agent': random_agent, }
        return headers

    def getPriceNow(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW".format(self.id), headers=self.headersUpdate())
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#main-0-QuoteHeader-Proxy .Mend\(16px\)")
            return u1[0].text
        else:
            return None

    def getProfile(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/profile".format(self.id), headers=self.headersUpdate())
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#main-2-QuoteProfile-Proxy section:nth-of-type(1) span>span")
            u2 = soup.select("#main-2-QuoteProfile-Proxy section:nth-of-type(1) span+div")
            for i in range(len(u1)):
                # print(u1[i].text,u2[i].text)
                self.listProfile[u1[i].text] = u2[i].text
            return self.listProfile
        else:
            return None

    def getGrossMargin(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/income-statement".format(self.id), headers=self.headersUpdate())
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#qsp-income-statement-table .table-header-wrapper > div")
            u2 = soup.select("#qsp-income-statement-table li:nth-of-type(1) span")
            u3 = soup.select("#qsp-income-statement-table li:nth-of-type(2) span")
            for i in range(1, len(u1)):
                quarter = u1[i].text.replace(" ", "")
                income = int(u2[i].text.replace(",", ""))
                grossProfit = int(u3[i].text.replace(",", ""))
                # grossMargin = grossProfit / income
                # print(quarter,income,gross_profit,gross_margin)
                self.listProfit[quarter] = {"quarter": quarter, "income": income, "gross_profit": grossProfit, "EPS": 0}
                year = quarter[0:4:1]
                if year in self.listDividend:
                    income += income
                    grossProfit += grossProfit
                    #grossMargin = grossProfit / income
                    self.listDividend[year]["income"] = income
                    self.listDividend[year]["gross_profit"] = grossProfit
                    #self.listDividend[year]["gross_margin"] = grossMargin
                else:
                    self.listDividend[year] = {"year": year, "income": income, "gross_profit": grossProfit, "EPS": 0, "cash_dividends": 0.0, "stock_dividends": 0.0, "payment":0}
            return True
        else:
            return None

    def getEps(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/eps".format(self.id), headers=self.headersUpdate())
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#qsp-eps-table li.List\(n\)>div>div:nth-of-type(1)")
            u2 = soup.select("#qsp-eps-table li.List\(n\)>div>div:nth-of-type(2)")
            for i in range(len(u1)):
                quarter = u1[i].text.replace(" ", "")
                eps = float(u2[i].text)
                if quarter in self.listProfit:
                    self.listProfit[quarter]["EPS"] = float(Decimal(self.listProfit[quarter]["EPS"]) + Decimal(eps))
                    #print("zzzzzzzzzzzzz",self.listProfit[quarter]["EPS"], eps)
                else:
                    self.listProfit[quarter] = {"quarter": quarter, "income": 0.0, "gross_profit": 0.0, "EPS": eps}
                year = quarter[0:4:1]
                if year in self.listDividend:
                    self.listDividend[year]["EPS"] = float(Decimal(self.listDividend[year]["EPS"]) + Decimal(eps))
                    #print(u1[i].text, eps)
                else:
                    self.listDividend[year] = {"year": year, "income": 0, "gross_profit": 0, "EPS": eps, "cash_dividends": 0.0, "stock_dividends": 0.0, "payment":0}
                    #print(u1[i].text, eps)
            #print(self.listDividend)
            #return self.listProfit
            return True
        else:
            return None

    def gerDividend(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/dividend".format(self.id), headers=self.headersUpdate())
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li div.Ta\(start\)")
            u2 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(2) span")
            u3 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(3) span")
            for i in range(len(u1)):
                # item = [u1[i].text,u2[i].text,u3[i].text]
                # self.listDividend.append(item)
                year = u1[i].text[0:4:1]
                try:
                    cashDividends = float(u2[i].text)
                except:
                    cashDividends = 0.0
                try:
                    stockDividends = float(u3[i].text)
                except:
                    stockDividends = 0.0
                if year in self.listDividend:
                    if self.listDividend[year]["cash_dividends"] == -1.0:
                        self.listDividend[year]["cash_dividends"] = 0.0
                    if self.listDividend[year]["stock_dividends"] == -1.0:
                        self.listDividend[year]["stock_dividends"] = 0.0
                    self.listDividend[year]["cash_dividends"] = float(Decimal(self.listDividend[year]["cash_dividends"]) + Decimal(cashDividends))
                    self.listDividend[year]["stock_dividends"] = float(Decimal(self.listDividend[year]["stock_dividends"]) + Decimal(stockDividends))
                    #print(u1[i].text, float(u2[i].text), float(u3[i].text))
                else:
                    self.listDividend[year] = {"year": year, "income": 0, "gross_profit": 0, "EPS": 0.0, "cash_dividends": cashDividends, "stock_dividends": stockDividends, "payment":0}
                    #print(u1[i].text, float(u2[i].text), float(u3[i].text))
            #print(self.listDividend)
            #return self.listDividend
            return True
        else:
            return None

    def getDividendPayment(self):
        url = 'https://mopsfin.twse.com.tw/opendata/t187ap45_L.csv'
        webpage = urllib.request.urlopen(url)
        data = csv.reader(webpage.read().decode('utf-8').splitlines())
        for i in data:
            if "出表日期" in i[0]:
                continue
            if i[0] == "":
                break
            self.listDividendPayment.append(i[1])
        return self.listDividendPayment

    def getProfit(self):
        if self.getGrossMargin() is not None and self.getEps() is not None and self.gerDividend() is not None:
            self.getDividendPayment()
            for item in list(self.listDividend.values()):
                year = int(item['year'])
                localeTime = time.gmtime().tm_year
                if year == localeTime or (year == localeTime - 1 and self.id not in self.listDividendPayment):
                    self.listDividend[str(year)]['payment'] = 0
                else:
                    self.listDividend[str(year)]['payment'] = 1
            return self.listDividend, self.listProfit
        else:
            return None

    def getCompany(self):
        url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=open_data'
        webpage = urllib.request.urlopen(url)
        data = csv.reader(webpage.read().decode('utf-8').splitlines())
        for i in data:
            if "證券代號" in i[0]:
                continue
            if i[0] == "":
                break
            # print('證券代號->',i[0],'證券名稱=',i[1], '殖利率(%)=',i[2],'股利年度=',i[3], '本益比=',i[4],'股價淨值比=',i[5], '財報年/季=',i[6])
            i[2] = 0.0 if i[2] == "" else float(i[2])
            i[3] = 0.0 if i[3] == "" else float(i[3])
            self.listCompany[i[0]] = {'id': i[0], 'name': i[1], 'd_yield': i[2], 'PE': i[3]}
        # self.listCompany.pop('證券代號',0)

    def getPrice(self):
        url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
        webpage = urllib.request.urlopen(url)
        data = csv.reader(webpage.read().decode('utf-8').splitlines())
        for i in data:
            # print('證券代號->',i[0],'證券名稱=',i[1], '成交股數=',i[2], '成交金額=',i[3],'開盤價=',i[4], '最高價=',i[5],'最低價=',i[6], '收盤價=',i[7], '漲跌價差=',i[8], '成交筆數=',i[9])
            if i[0] in self.listCompany:
                i[7] = 0.0 if i[7] == "" else float(i[7])
                newData = GetData().getLastDividend(i[0])
                self.listCompany[i[0]]['price'] = i[7]
                if newData != 0 and i[7]!=0:
                    self.listCompany[i[0]]['PE'] = newData[1]
                    self.listCompany[i[0]]['d_yield'] = round((newData[0]/i[7])*10000)/100
            if i[0] == "":
                break
        # print(self.listCompany)

    def getStockInfo(self):
        self.getCompany()
        self.getPrice()
        return self.listCompany



class UpdateData:
    def __init__(self):
        self.listInfo = Spider().getStockInfo()
        self.listStockId = list()
        self.dbFile = 'yield.db'
        # print(self.listInfo)

    def createConnection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbFile)
        except sqlite3Error as e:
            print("sqlite連線錯誤")
            print(e)
            return
        return conn

    def createProfitTable(self, conn):
        sql = '''
            CREATE TABLE IF NOT EXISTS profit(
                id TEXT PRIMARY KEY,
                stock_id TEXT,
                quarter TEXT,
                income INTEGER,
                gross_profit INTEGER,
                EPS REAL
            );
            '''

        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except sqlite3Error as e:
            print(e)

    def replaceProfitData(self, conn, id, dataList):
        sql = '''
        INSERT or replace INTO 
        profit(id,stock_id,quarter,income,gross_profit,EPS)
        VALUES( ?,?,?,?,?,?)
        '''.format(id)

        try:
            curser = conn.cursor()
            for item in dataList.values():
                print(item)
                pid = id + item['quarter']
                stock_id = id
                quarter = item['quarter']
                income = item['income']
                gross_profit = item['gross_profit']
                EPS = item['EPS']
                curser.execute(sql, (pid, stock_id, quarter, income, gross_profit, EPS))
        except  sqlite3Error as e:
            print(e)
        conn.commit()

    def createDividendTable(self, conn):
        sql = '''
            CREATE TABLE IF NOT EXISTS dividend(
                id TEXT PRIMARY KEY,
                stock_id TEXT,
                year TEXT,
                income INTEGER,
                gross_profit INTEGER,
                EPS REAL,
                cash_dividends REAL,
                stock_dividends REAL,
                payment INTEGER
            );
            '''
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except sqlite3Error as e:
            print(e)

    def replaceDividendData(self, conn, id, dataList):
        sql = '''
        INSERT or replace INTO 
        dividend(id,stock_id,year,income,gross_profit,EPS,cash_dividends,stock_dividends,payment)
        VALUES( ?,?,?,?,?,?,?,?,?)
        '''.format(id)

        try:
            curser = conn.cursor()
            for item in dataList.values():
                print(item)
                pid = id + item['year']
                stock_id = id
                year = item['year']
                income = item['income']
                gross_profit = item['gross_profit']
                EPS = item['EPS']
                cash_dividends = item['cash_dividends']
                stock_dividends = item['stock_dividends']
                payment = item['payment']
                curser.execute(sql, (pid, stock_id,year, income, gross_profit, EPS, cash_dividends, stock_dividends, payment))
        except  sqlite3Error as e:
            print(e)
        conn.commit()

    def updateProfitAndDividendInfo(self, id, autoUpdateRecord=True):
        dividend, profit = Spider(id).getProfit()
        conn = self.createConnection()
        update_time = int("{:0>4}{:0>2}{:0>2}".format(time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday))
        updateRecord = {"id":"stock","stock_id":id,"update_time":update_time}
        with conn:
            self.createProfitTable(conn)
            self.replaceProfitData(conn, id, profit)
            self.createDividendTable(conn)
            self.replaceDividendData(conn, id, dividend)
            if autoUpdateRecord:
                #self.createUpdateRecordTable(conn)
                self.replaceUpdateRecordData(conn, updateRecord)

    def createUpdateRecordTable(self, conn):
        sql = '''
             CREATE TABLE IF NOT EXISTS update_record(
                id TEXT PRIMARY KEY,
                stock_id TEXT NOT NULL,
                update_time INTEGER
            );
            '''
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except sqlite3Error as e:
            print(e)

    def replaceUpdateRecordData(self, conn, item):
        sql = '''
            INSERT or replace INTO 
            update_record(id,stock_id,update_time)
            VALUES( ?,?,?)
            '''
        try:
            curser = conn.cursor()
            id = item['id']
            stock_id = item['stock_id']
            update_time = item['update_time']
            curser.execute(sql, ( id, stock_id, update_time))
        except  sqlite3Error as e:
            print(e)
        conn.commit()

    def createStockTable(self, conn):
        sql = '''
            CREATE TABLE IF NOT EXISTS stock(
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                d_yield REAL,
                PE REAL,
                price REAL,
                time_to_market TEXT,
                classification TEXT,
                share_capital INTEGER,
                IHOLD REAL,
                update_time INTEGER,
                UNIQUE (name)
            );
            '''
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except sqlite3Error as e:
            print(e)

    def replaceStockData(self, conn, item):
        sql = '''
        INSERT or replace INTO 
        stock(id,name,d_yield,PE,price,time_to_market,classification,share_capital,IHOLD,update_time)
        VALUES( ?,?,?,?,?,?,?,?,?,?)
        '''

        try:
            curser = conn.cursor()
            id = item['id']
            name = item['name']
            d_yield = item['d_yield']
            PE = item['PE']
            price = item['price']
            time_to_market = item['time_to_market']
            classification = item['classification']
            share_capital = item['share_capital']
            IHOLD = item['IHOLD']
            update_time = item['update_time']
            curser.execute(sql, (
            id, name, d_yield, PE, price, time_to_market, classification, share_capital, IHOLD, update_time))
        except  sqlite3Error as e:
            print(e)
        conn.commit()

    def checkStockCount(self, conn, id):
        sql = '''
        SELECT count(*)
        FROM stock
        WHERE id = '{}'
        '''.format(id)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            # print(row[0])
        except sqlite3Error as e:
            print(e)
        return row[0]

    def getStockData(self, conn, id):
        sql = '''
                SELECT *
                FROM stock
                WHERE id = '{}'
                '''.format(id)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            print(row)
        except sqlite3Error as e:
            print(e)
        return row

    def updateCompanyInfo(self,item):
        #for item in list(self.listInfo.values()):
            self.listStockId.append(item['id'])
            conn = self.createConnection()
            updateTime = int(
                "{:0>4}{:0>2}{:0>2}".format(time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday))
            with conn:
                self.createUpdateRecordTable(conn)
                self.createStockTable(conn)
                ctype = 99
                stock = self.getStockData(conn, item['id'])
                if self.checkStockCount(conn, item['id']) == 0:
                    ctype = 0
                elif updateTime - 7 > stock[9] or (time.gmtime().tm_mday % 5 == 0 and updateTime != stock[9]):
                    ctype = 0
                elif updateTime != stock[9]:
                    ctype = 1
                if ctype == 99:
                    return
                elif ctype == 0:
                    newInfo = Spider(item['id']).getProfile()
                    item['time_to_market'] = newInfo['上市時間'] or ""
                    item['classification'] = newInfo['產業類別'] or ""
                    item['share_capital'] = newInfo['股本'] or "0"
                    item['share_capital'] = int(item['share_capital'].replace(",", ""))
                    item['IHOLD'] = newInfo['董監持股比例(%)'] or "0.0"
                    item['IHOLD'] = float(item['IHOLD'])
                    time.sleep(3)
                else:
                    item['time_to_market'] = stock[5]
                    item['classification'] = stock[6]
                    item['share_capital'] = stock[7]
                    item['IHOLD'] = stock[8]
                item['update_time'] = updateTime
                #self.listStockId.append(item['id'])
                self.replaceStockData(conn, item)

    def createDatabase(self):
        for item in list(self.listInfo.values()):
            self.updateCompanyInfo(item)
        r = GetData().getUpdateRecord("stock")
        updateTime = int("{:0>4}{:0>2}{:0>2}".format(time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday))
        index = 0
        if r[0] in self.listStockId:
            index = self.listStockId.index(r[0])
        if updateTime - 7 > r[1]:
            index = 0
        for i in range(index,len(self.listStockId)):
            #self.updateProfitAndDividendInfo(self.listStockId[i])
            self.updateProfitAndDividendInfo(self.listStockId[i])
            time.sleep(5)

class GetData(UpdateData):
    def __init__(self):
        self.dbFile = 'yield.db'

        # print(self.listInfo)

    def createConnection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbFile)
        except sqlite3Error as e:
            print("sqlite連線錯誤")
            print(e)
            return
        return conn

    def getUpdateRecord(self, id):
        conn = self.createConnection()
        sql = f'''
            SELECT stock_id,update_time
            FROM update_record
            WHERE id = '{id}'
            '''
        rows = list()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                rows = cursor.fetchone()
                # print(rows)
            except sqlite3Error as e:
                print(e)
        if rows is None or len(rows) == 0:
            return 0
        else:
            return rows

    def getListStock(self,key):
        conn = self.createConnection()
        sql = f'''
            SELECT id,name,classification,d_yield,price
            FROM stock
            WHERE {key}
            '''
        rows = list()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                #print(rows)
            except sqlite3Error as e:
                print(e)
        return rows


    def getSumInfo(self,id):
        conn = self.createConnection()
        sql = '''
            SELECT EPS,cash_dividends,stock_dividends
            FROM dividend
            WHERE payment = 1 AND stock_id = '{}'
            limit 0, 5
            '''.format(id)
        rows = list()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                #print(rows)
            except sqlite3Error as e:
                print(e)
        return rows

    def getListDividend(self,id):
        conn = self.createConnection()
        sql = '''
            SELECT year,income,gross_profit,EPS,cash_dividends,stock_dividends
            FROM dividend
            WHERE payment = 1 AND stock_id = '{}'
            '''.format(id)
        rows = list()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                # print(rows)
            except sqlite3Error as e:
                print(e)
        return rows

    def getListProfit(self,id):
        conn = self.createConnection()
        sql = '''
            SELECT quarter,income,gross_profit,EPS
            FROM profit
            WHERE stock_id = '{}'
            '''.format(id)
        rows = list()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                # print(rows)
            except sqlite3Error as e:
                print(e)
        return rows

    def getStockInfo(self,id):
        UpdateData().updateProfitAndDividendInfo(id,False)
        conn = self.createConnection()
        sql = '''
            SELECT id,name,price,time_to_market,classification,share_capital,IHOLD
            FROM stock
            WHERE id = '{}'
            '''.format(id)
        rows = list()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                rows = cursor.fetchone()
                # print(rows)
            except sqlite3Error as e:
                print(e)
        return rows

    def getLastDividend(self,id):
        conn = self.createConnection()
        sql = '''
            SELECT cash_dividends,year
            FROM dividend
            WHERE payment = 1 AND stock_id = '{}'
            limit 0, 1
            '''.format(id)
        rows = list()
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                rows = cursor.fetchone()
                print(rows)
            except sqlite3Error as e:
                print(e)
        if rows is None or len(rows) == 0:
            return 0
        else:
            return rows



"""
條件1：股本 > 50 億元以上

條件2：近 10 年平均現金股利發放率 > 50%

條件3：近 10 年平均現金股利殖利率 > 6%

條件4：近 10 年每年 EPS > 1 元以上

本益比= 股價/每股盈餘
"""
