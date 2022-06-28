from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv
ssl._create_default_https_context = ssl._create_unverified_context
heads = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

while True:
    url = "https://goldprice.org/cryptocurrency-price"
    import_request = Request(url, headers=heads)
    web_page_data = urlopen(import_request).read()

    soup = BeautifulSoup(web_page_data, 'html.parser')
    all_groups=soup.find_all('td',attrs={"class":"views-field views-field-field-crypto-price-1 views-align-right"})
    bit_object = all_groups[0]
    ethe_object = all_groups[1]
    bit=bit_object.string
    bit = bit.strip()
    ethe=ethe_object.string
    ethe = ethe.strip()
    all_changes = soup.find_all('td',attrs={"class":"views-field views-field-field-crypto-price-change-pc-24h views-align-right"})
    bit_change_object = all_changes[0]
    ethe_change_object = all_changes[1]
    bit_change=bit_change_object.string
    bit_change = bit_change.strip()
    ethe_change=ethe_change_object.string
    ethe_change=ethe_change.strip()
    #存檔
    now = datetime.now()
    file_name = now.strftime("%Y-%m-%d_crypto.csv")
    now_string = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name,'a',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["bitcoin",now_string,bit,bit_change])

        writer.writerow(["Ethereum",now_string,ethe,ethe_change])

    time.sleep(60)