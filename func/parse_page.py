from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import pandas as pd
import time

URL = 'https://www.cian.ru/sale/flat/292125772/'


def get_name(main):
    try:
        return main.find('h1', class_='a10a3f92e9--title--vlZwT').text
    except Exception as e:
        return e


def get_price(main):
    try:
        return main.find('div', class_='a10a3f92e9--amount--ON6i1').text
    except Exception as e:
        return e


def get_float(main):
    try:
        return main.find('div', class_='a10a3f92e9--group--K5ZqN').text
    except Exception as e:
        return e


def get_house(main):
    try:
        return main.find('div', class_='a10a3f92e9--group--K5ZqN a10a3f92e9--right--_9uBM').text
    except Exception as e:
        return e


def get_price_info(main):
    try:
        return main.find('div', class_='a10a3f92e9--item--n_zVq').text
    except Exception as e:
        return e


def get_page(url):
    r = requests.get(url)
    bs = BeautifulSoup(r.content, features='html.parser')
    data = {
        'name' : get_name(bs),
        'price' : get_price(bs),
        'price_info' : get_price_info(bs),
        'float' : get_float(bs),
        'house' : get_house(bs)
    }
    for key in data:
        if isinstance(data[key], Exception):
            return key, data[key]
    else:
        return data


if __name__ == '__main__':
    print(get_page(URL))
