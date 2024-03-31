from bs4 import BeautifulSoup
import requests
import json
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import pandas as pd
import time

# URL = 'https://www.cian.ru/sale/flat/292125772/'
URL = 'https://www.cian.ru/sale/flat/295473855/'


def get_name(main):
    try:
        return main.find('h1', class_='a10a3f92e9--title--vlZwT').text[:-2]
    except Exception as e:
        return e


def get_price(main):
    try:
        price_not_valid = main.find('div', class_='a10a3f92e9--amount--ON6i1').text
        return int(''.join(filter(str.isdigit, price_not_valid)))
    except Exception as e:
        return e


def get_float(main):
    try:
        data = [val.text for val in main.find('div', class_='a10a3f92e9--group--K5ZqN').
        find_all('div', class_='a10a3f92e9--item--qJhdR')]
        return data
    except Exception as e:
        return e


def get_house(main):
    try:
        return [val.text for val in main.find('div', class_='a10a3f92e9--group--K5ZqN a10a3f92e9--right--_9uBM').
        find_all('div', class_='a10a3f92e9--item--qJhdR')]
    except Exception as e:
        return e


def get_price_info(main):
    try:
        import re
        def extract_digits(input_string):
            cleaned_string = re.sub(r'[^0-9]', '', input_string)
            # digits = ''.join(filter(str.isdigit, cleaned_string))
            return 'Цена за метр ', cleaned_string

        data = [val.text for val in main.find_all('div', class_='a10a3f92e9--item--iWTsg')]
        data[0] = extract_digits(data[0])
        # text = data[2]
        data[2] = data[2][:7] + ' ' + data[2][7:]
        return data
    except Exception as e:
        return e


def get_photos(main):
    def check_link(url):
        try:
            response = requests.head(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    try:
        # div_tag = main.find('div', {'id': 'photos'})
        # links = [src.get('src') for src in div_tag.find_all('img')]
        # valid_links = [link for link in links if check_link(link)]

        img_tags = main.find_all('img', {'loading': 'lazy'})
        links = [src.get('src') for src in img_tags]
        valid_links = [link for link in links if check_link(link)]

        return list(set(valid_links))
    except Exception as e:
        return e


def get_address(main):
    try:
        address = main.find('div', class_='a10a3f92e9--address-line--GRDTb').text
        address = address.replace(',', '')
        address = address.replace('На карте', '')
        return address
    except Exception as e:
        return e


def get_page(url):
    r = requests.get(url)
    bs = BeautifulSoup(r.content, features='html.parser')
    data = {
        'name': get_name(bs),
        'price': get_price(bs),
        'price_info': get_price_info(bs),
        'float': get_float(bs),
        'house': get_house(bs),
        'addres': get_address(bs),
        'photos': get_photos(bs),
        'link': url
    }
    for key in data:
        if isinstance(data[key], Exception):
            return key, data[key]
    else:
        return data


def save_dict_to_json(dictionary, file_name):
    # Проверяем существует ли файл
    if os.path.exists(file_name):
        # Если файл существует, читаем данные из него
        with open(file_name, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)

        # Обновляем существующие данные новыми данными из словаря
        existing_data.append(dictionary)
        data_to_write = existing_data
    else:
        # Если файл не существует, используем только новый словарь
        data_to_write = dictionary

    # Записываем словарь в файл в формате JSON
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data_to_write, file, ensure_ascii=False, indent=4)


def parse_links(links: str, num_page=0):
    import pandas as pd
    df_links = pd.read_csv(links)
    for i in range(num_page, len(df_links)):
        print(i)
        # print(df_links.iloc[i].links)
        data = get_page(df_links.iloc[i].links)
        print(data)
        if not isinstance(data, tuple):
            save_dict_to_json(data, 'parse1.json')
        time.sleep(5)


if __name__ == '__main__':
    # test_data = get_page(URL)
    # print(test_data)
    # save_dict_to_json(test_data, 'parse_page.json')
    parse_links(links='links.csv', num_page=0)
