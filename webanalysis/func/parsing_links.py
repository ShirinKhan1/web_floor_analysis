import csv

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import pandas as pd
import time

URL = 'https://www.cian.ru/cat.php?bbox=55.81272906727757%2C37.3338023710937%2C55.916019150829065%2C37.844666628906204&center=55.86440858670469%2C37.58923449999994&deal_type=sale&engine_version=2&in_polygon[0]=37.3931972_55.8261039%2C37.4096767_55.8233971%2C37.4302761_55.8218504%2C37.4495022_55.8222371%2C37.4714748_55.8237838%2C37.4907009_55.8264906%2C37.509927_55.829584%2C37.531213_55.8330641%2C37.5497524_55.8353842%2C37.5710384_55.8357709%2C37.5943844_55.8349975%2C37.6156704_55.8342242%2C37.6348965_55.8334508%2C37.6548092_55.8326774%2C37.6719753_55.8338375%2C37.6898281_55.8373176%2C37.7063076_55.8415711%2C37.7317135_55.8473713%2C37.7488796_55.8516248%2C37.7626125_55.857425%2C37.7763454_55.8678653%2C37.7852718_55.8759856%2C37.7626125_55.8844926%2C37.7426998_55.8883594%2C37.7262203_55.8899061%2C37.7076809_55.8910661%2C37.6912014_55.8949329%2C37.6767818_55.9007331%2C37.6603023_55.9042133%2C37.6431362_55.9065333%2C37.6225368_55.9065333%2C37.6012508_55.9065333%2C37.5833981_55.9065333%2C37.5662319_55.90692%2C37.5483791_55.9065333%2C37.5318996_55.9053733%2C37.5154201_55.9038266%2C37.5003139_55.8999598%2C37.4907009_55.8922262%2C37.476968_55.8848793%2C37.4625484_55.8790791%2C37.4467556_55.8763723%2C37.4302761_55.8721188%2C37.4179165_55.8655452%2C37.4028103_55.8616784%2C37.3945705_55.8531715%2C37.3931972_55.8435045%2C37.3945705_55.8342242%2C37.3931972_55.8261039&offer_type=flat&origin=map&polygon_name[0]=Область%20поиска&zoom=12'

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


def parse_links(url, filename, page=1):
    file = None
    try:
        file = pd.read_csv(filename)
    except FileNotFoundError:
        pd.DataFrame(columns=['links']).to_csv(filename)

    for i in range(page, MAX + 1):
        links = get_links(url, i)
        print(str(i) + ' ' + str(links))
        file = pd.concat([file, pd.DataFrame(data=links, columns=['links'])])
        file.to_csv(filename, index=False)
        time.sleep(30)

    print("Done!")


if __name__ == '__main__':
    parse_links(URL, filename='links_12-04-2024.csv', page=4)
