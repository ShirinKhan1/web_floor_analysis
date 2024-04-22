import csv

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import pandas as pd
import time
from parse_page import get_page
from fix_data_after_parsing import fix_data_after_parsing
from convert_to_csv import final_fix
URL = 'https://www.cian.ru/cat.php?bbox=55.7205895065%2C37.6007840756%2C55.7573424115%2C37.7614591244&deal_type=sale&engine_version=2&in_polygon%5B1%5D=37.6618955_55.7339302%2C37.6673887_55.7304427%2C37.6749418_55.7277301%2C37.6838682_55.7257926%2C37.6927946_55.7250176%2C37.7010343_55.7254051%2C37.7079008_55.7281176%2C37.7079008_55.7339302%2C37.7037809_55.7381928%2C37.6989744_55.7424554%2C37.6941679_55.7467179%2C37.6886747_55.750593%2C37.6811216_55.7525305%2C37.6728818_55.752918%2C37.6653287_55.7509805%2C37.6577756_55.749043%2C37.6543424_55.7447804%2C37.6577756_55.7401303%2C37.6605222_55.7354803%2C37.6618955_55.7339302&offer_type=flat&polygon_name%5B1%5D=Область+поиска&room1=1&room2=1&room3=1'

MAX = 54


def get_links(url, page=None):
    while True:
        r = requests.get(url)
        if not (page is None):
            r = requests.get(url + '&page=' + str(page))
        bs = BeautifulSoup(r.content, 'html.parser')
        a_href = bs.find_all('a', class_='_93444fe79c--media--9P6wN')
        links = [a.get('href') for a in a_href]
        if links:
            return links
        else:
            print('list in null!! =(')
            # print(r.text)
            time.sleep(60)


def parse_links(url, num=1):
    # with open('links.csv', mode='w', newline='', encoding='utf-8') as file:
    file = pd.read_csv('links.csv')
        # writer = csv.writer(file)
        # writer.writerow(['links'])
    for i in range(num, MAX + 1):
        links = get_links(url, i)
        print('We got list of links: ' + str(len(links)))
        # print(str(i) + ' ' + str(links))
        for link in links:
            print(link)
            data = get_page(link)
            print('Function get_page was done completely!')
            if not isinstance(data, tuple):
                data = final_fix(fix_data_after_parsing(data))
                print(data)
                time.sleep(40)
            else:
                print('Error \n' + str(data))
        time.sleep(30)

    print("Done!")


if __name__ == '__main__':
    parse_links(URL)
