from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
import time
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
    print(bit_object.string)
    print(ethe_object.string)
    all_changes = soup.find_all('td',attrs={"class":"views-field views-field-field-crypto-price-change-pc-24h views-align-right"})
    bit_change_object = all_changes[0]
    ethe_change_object = all_changes[1]
    print(bit_change_object.string)
    print(ethe_change_object.string)
    time.sleep(60)