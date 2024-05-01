import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
from func.parse_page import get_page
from func.fix_data_after_parsing import fix_data_after_parsing
from func.convert_to_csv import final_fix
from sqlalchemy import create_engine, text

URL = 'https://www.cian.ru/cat.php?bbox=55.6154932393%2C36.9718026547%2C55.9093373508%2C38.2572030453&deal_type=sale&engine_version=2&in_polygon%5B1%5D=37.405076_55.8497561%2C37.4023294_55.8396793%2C37.3940897_55.8296026%2C37.3899698_55.8203009%2C37.3844766_55.809449%2C37.3844766_55.7985971%2C37.3844766_55.7885204%2C37.3844766_55.7776685%2C37.3844766_55.7675917%2C37.3872232_55.75829%2C37.3913431_55.7489884%2C37.3940897_55.7396868%2C37.4009561_55.72961%2C37.4105692_55.7195332%2C37.4201822_55.7117819%2C37.4311685_55.7040305%2C37.4449014_55.6970543%2C37.4600076_55.6908532%2C37.4764871_55.6854273%2C37.4943399_55.6807764%2C37.5094461_55.6769008%2C37.5272989_55.6730251%2C37.5506449_55.6706997%2C37.5684976_55.6683743%2C37.5877237_55.6660489%2C37.6083231_55.6629483%2C37.6289224_55.6606229%2C37.6454019_55.6590726%2C37.6632547_55.6582975%2C37.6838541_55.6582975%2C37.7017069_55.6590726%2C37.7195596_55.661398%2C37.7374124_55.6644986%2C37.749772_55.6706997%2C37.7648783_55.678451%2C37.7772379_55.6846521%2C37.7882242_55.6916283%2C37.8019571_55.7001548%2C37.8143167_55.7094565%2C37.8239298_55.7187581%2C37.8307962_55.72961%2C37.8362894_55.7404619%2C37.8404093_55.7497636%2C37.8431558_55.7598403%2C37.8445291_55.7699171%2C37.8431558_55.7792187%2C37.8376627_55.7885204%2C37.8266763_55.797822%2C37.8129434_55.8071236%2C37.7950907_55.814875%2C37.7799845_55.8210761%2C37.7621317_55.8272772%2C37.7483988_55.8327031%2C37.7332926_55.8373539%2C37.7154398_55.8420048%2C37.6989603_55.8458804%2C37.6797342_55.8513064%2C37.6591348_55.8567323%2C37.6399088_55.860608%2C37.6206827_55.8637086%2C37.4188089_55.8668091%2C37.4078226_55.8598329%2C37.405076_55.8505312%2C37.405076_55.8497561&offer_type=flat&polygon_name%5B1%5D=Область+поиска&room1=1&room2=1&room9=1&sort=creation_date_desc'


# def get_info(href: str):
#     r = requests.get(href)
#     bs = BeautifulSoup(r.content, 'html.parser')
def extract_data(link, engine, url, method, user_id, datetimedttm,):
    with (engine.connect() as conn):
        data = get_page(link)
        print('Function get_page was done completely!')
        if not isinstance(data, tuple):
            print(data)
            data = final_fix(fix_data_after_parsing(data))
            print(data)
            # data.to_csv(f'data{i}.csv', index=False)
            try:
                stmt = text(f"SELECT id, link FROM float_float WHERE link = '{data.link[0]}'")
                result = conn.execute(stmt)
                if result.rowcount == 0:
                    data.to_sql('float_float', engine, if_exists='append', index=False)
                history = conn.execute(stmt)
                stmt2 = text(f"SELECT id FROM float_linkarea WHERE link = '{url}'")
                result2 = conn.execute(stmt2)
                if result2.rowcount == 0:
                    pd.DataFrame({'link': [url]}).to_sql('float_linkarea',
                                                         engine, if_exists='append', index=False)
                result2 = conn.execute(stmt2)
                hist_user = {
                    'float_id': [history.first()[0]],
                    'user_id': [user_id],
                    'method': [method],
                    'create_date_dttm': [datetimedttm],
                    'linkarea_id': [result2.first()[0]]
                }
                print(hist_user)
                pd.DataFrame(hist_user).to_sql('float_history',
                                               engine, if_exists='append', index=False)
            except Exception as e:
                print(e)
            time.sleep(40)
        else:
            print('Error \n' + str(data))


def parse(url):
    # a_href = bs.find('a', class_='_93444fe79c--link--VtWj6')
    # return a_href.get('href')
    while True:
        try:
            r = requests.get(url)
            bs = BeautifulSoup(r.content, 'html.parser')
            a_tag = bs.find('a', class_='_93444fe79c--link--VtWj6')
            return a_tag.get('href')
        except Exception as e:
            print('error!.. ', e)
            time.sleep(60)


def monitoring(url, check=False):
    parsed_url = urlparse(url)
    if check:
        return True if parsed_url.hostname == 'www.cian.ru' else False
    if parsed_url.hostname == 'www.cian.ru':
        query_parameters = parse_qs(parsed_url.query)
        try:
            if query_parameters['sort'][0] == "creation_date_desc":
                return parse(url)
            else:
                query_parameters['sort'][0] = 'creation_date_desc'
                updated_query = urlencode(query_parameters, doseq=True)
                url = urlunparse(
                    (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query,
                     parsed_url.fragment))
        except KeyError:
            url += '&sort=creation_date_desc'
    return False


def streaming(url: str, method, user_id, datetimedttm, finish=30, ):
    print('checking url...')
    if monitoring(url, check=True):
        print('url is valid')
        engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
        start = time.time()
        data = monitoring(url)
        while start - time.time() < finish * 60:
            print(time.time() * 60)
            new_data = monitoring(url)
            if new_data != data:
                # позже сделать подлючение к бд и записывать найденные квартиры в таблицу
                print(new_data)
                data = new_data
                extract_data(data, engine, url, method, user_id, datetimedttm)
            time.sleep(90)
    else:
        print('URL IS INVALID!!! ')


if __name__ == '__main__':
    # print(parse(URL))
    streaming(URL)
    # print(parse(URL))
