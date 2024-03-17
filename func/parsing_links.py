import csv

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import pandas as pd
import time

URL = 'https://www.cian.ru/cat.php?bbox=55.0741272496%2C35.4273483126%2C56.2524002714%2C40.5689498751&deal_type=sale&engine_version=2&offer_type=flat&p=2&region=1'

MAX = 54


def get_links(url, page=None):
    r = requests.get(url)
    if not (page is None):
        r = requests.get(url + '&page=' + str(page))
    bs = BeautifulSoup(r.content, 'html.parser')
    a_href = bs.find_all('a', class_='_93444fe79c--media--9P6wN')
    return [a.get('href') for a in a_href]


def parse_links(url):
    with open('links.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['links'])

        for i in range(1, MAX + 1):
            links = get_links(URL, i)
            print(str(i) + ' ' + str(links))
            for link in links:
                writer.writerow([link])
            # time.sleep(5)

    print("Done!")


if __name__ == '__main__':
    pass
