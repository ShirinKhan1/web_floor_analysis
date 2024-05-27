from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

from sqlalchemy import create_engine, text

from parse_page import get_price_info, get_house, get_float, get_address, get_floor, get_city

MAX = 54
URL = 'https://www.cian.ru/cat.php?center=55.70077286336706%2C37.807089951820664&deal_type=rent&district[0]=8&engine_version=2&offer_type=flat&room1=1&room2=1&type=4&zoom=12&origin=map'
URL_FLOAT = 'https://www.cian.ru/rent/flat/301559426/'


def get_links(url, page=None):
    while True:
        r = requests.get(url)
        if not (page is None):
            r = requests.get(url + '&page=' + str(page))
        bs = BeautifulSoup(r.content, 'html.parser')
        a_href = bs.find_all('a', class_='_93444fe79c--link--VtWj6')
        links = [a.get('href') for a in a_href]
        if links:
            return links
        else:
            print('list in null!! =(')
            # print(r.text)
            time.sleep(60)


def get_name(main):
    try:
        name = main.find('h1', class_='a10a3f92e9--title--vlZwT').text
        if name:
            return name
        else:
            raise ValueError
    except Exception as e:
        return e


def get_price(main):
    try:
        price_not_valid = main.find(attrs={'data-testid': 'price-amount'}).text
        price = int(''.join(filter(str.isdigit, price_not_valid)))
        if price:
            return price
        else:
            raise ValueError
    except Exception as e:
        return e


def get_inventory(main):
    try:
        inv = []
        div_tg = main.find('div', class_='a10a3f92e9--wrapper--Ycswz').find_all('div')
        for div in div_tg:
            inv.append(div.text.strip())
        return ', '.join(inv)
    except Exception as e:
        return e


def get_room(name: str):
    name = name.split(sep=',')[0]
    if 'студия' in name.lower():
        return 0
    else:
        return int(name[len('Сдается '):].split(sep='-комн')[0])


def get_float_rent(main):
    try:
        data = [val.text for val in main.find('table', class_='a10a3f92e9--group--K5ZqN')
        .find_all('tr', class_='a10a3f92e9--item--qJhdR')]
        return [x for x in data if 'лощадь' in x]
    except Exception as e:
        return e


def get_page_rent(url):
    r = requests.get(url)
    bs = BeautifulSoup(r.content, features='html.parser')
    data = {
        'name': [get_name(bs)],
        'price': [get_price(bs)],
        # 'inventory': get_inventory(bs),
        'float': get_float_rent(bs),
        # 'house': get_house(bs),
        'address': [get_address(bs)],
        'link': [url],
        'cntroom': [get_room(get_name(bs))],
        'city': [get_city(get_address(bs))[0]],
        'district': [get_city(get_address(bs))[1]],

    }
    for key in data:
        if isinstance(data[key], Exception):
            return key, data[key]
    else:
        return data


def fix_data(fl: dict):
    for val in fl['float']:
        val = val.replace(',', '.')
        if 'Общая площадь' in val:
            l = len('Общая площадь')
            fl['totalarea'] = [float(val[l:])]
        elif 'Жилая площадь' in val:
            l = len('Жилая площадь')
            fl['livingarea'] = [float(val[l:])]
        elif 'Площадь кухни' in val:
            l = len('Площадь кухни')
            fl['kitchenarea'] = [float(val[l:])]
    fl.pop('float')
    return fl


def parse_links(url, num=1):
    engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
    with (engine.connect() as conn):
        for i in range(num, MAX + 1):
            links = get_links(url, i)
            print('We got list of links: ' + str(len(links)))
            # print(str(i) + ' ' + str(links))
            for link in links:
                print(link)
                try:
                    data = get_page_rent(link)
                    print('Function get_page was done completely!')
                    if not isinstance(data, tuple):

                        # print(data)
                        try:
                            data = pd.DataFrame(fix_data(data))
                            stmt = text(f"SELECT id, link FROM float_floatrent WHERE link = '{data.link[0]}'")
                            result = conn.execute(stmt)
                            if result.rowcount == 0:
                                data.to_sql('float_floatrent', engine, if_exists='append', index=False)
                        except Exception as e:
                            print(e)
                        time.sleep(40)
                    else:
                        print('Error \n' + str(data))
                except Exception as e:
                    pass
            # Вставьте данные из DataFrame в базу данных
            time.sleep(30)

    print("Done!")


if __name__ == '__main__':
    url_rostov = 'https://rostov.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&region=4959&room3=1&room4=1&room5=1&type=4'
    url_msk = 'https://www.cian.ru/cat.php?deal_type=rent&district%5B0%5D=1&district%5B1%5D=5&district%5B2%5D=6&district%5B3%5D=11&district%5B4%5D=325&district%5B5%5D=326&engine_version=2&offer_type=flat&p=1&room3=1&room4=1&room5=1&type=4'
    # test_data = get_page_rent(URL_FLOAT)
    # print(test_data)
    # test_data = fix_data(test_data)
    # print(test_data)
    # parse_links(url_rostov)
    parse_links(url_msk)
    # save_dict_to_json(test_data, 'parse_page.json')
    # parse_links(links='links.csv', num_page=1055)
