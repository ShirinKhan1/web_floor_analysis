import csv

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import pandas as pd
import time
from func.parse_page import get_page
from func.fix_data_after_parsing import fix_data_after_parsing
from func.convert_to_csv import final_fix
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, select, text
URL = 'https://www.cian.ru/cat.php?bbox=55.80469403655583%2C37.35409257558594%2C55.84136740011852%2C37.51476762441408&center=55.82303505795017%2C37.43443010000002&deal_type=sale&engine_version=2&in_polygon[0]=37.3951196_55.8288314%2C37.3982095_55.8270913%2C37.4012994_55.8249646%2C37.4043893_55.8232245%2C37.4074792_55.8214844%2C37.4105691_55.8199376%2C37.4143457_55.8187776%2C37.4184656_55.8174242%2C37.4225854_55.8162641%2C37.426362_55.8151041%2C37.4301385_55.813944%2C37.4335718_55.8125906%2C37.4373483_55.8114306%2C37.4411249_55.8104639%2C37.4449014_55.8094971%2C37.4483346_55.8079504%2C37.4521112_55.8069837%2C37.4565744_55.8062103%2C37.4610376_55.8058236%2C37.4651575_55.8056303%2C37.4692773_55.806597%2C37.4716806_55.8087238%2C37.4733972_55.8110439%2C37.4740839_55.813364%2C37.4740839_55.8164575%2C37.4740839_55.8189709%2C37.4740839_55.8214844%2C37.4733972_55.8239978%2C37.4723672_55.826318%2C37.4709939_55.8286381%2C37.4692773_55.8309582%2C37.4668741_55.8330849%2C37.4630975_55.8346317%2C37.4589777_55.8359851%2C37.4541711_55.8369518%2C37.4500513_55.8375318%2C37.4459314_55.8379185%2C37.4418115_55.8383052%2C37.4373483_55.8386919%2C37.4328851_55.8392719%2C37.4280786_55.8396586%2C37.4239587_55.8398519%2C37.4198389_55.8402386%2C37.415719_55.840432%2C37.4112558_55.840432%2C37.4071359_55.8394653%2C37.403016_55.8384985%2C37.3995828_55.8371451%2C37.3964929_55.8355984%2C37.3951196_55.8332783%2C37.3947763_55.8309582%2C37.3951196_55.8288314&offer_type=flat&origin=map&polygon_name[0]=Область%20поиска&room1=1&room2=1&room9=1&zoom=14'

MAX = 54
# MAX = 30


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


def parse_links(url, method, user_id, datetimedttm, num=1):
    engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
    with (engine.connect() as conn):

        for i in range(num, MAX + 1):
            links = get_links(url, i)
            print('We got list of links: ' + str(len(links)))
            # print(str(i) + ' ' + str(links))
            for link in links:
                print(link)
                try:
                    data = get_page(link)
                    print('Function get_page was done completely!')
                    if not isinstance(data, tuple):

                        # print(data)
                        try:
                            data = final_fix(fix_data_after_parsing(data))
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
                            pd.DataFrame(hist_user).to_sql('float_history',
                                                           engine, if_exists='append', index=False)
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
    URL_vorosh = 'https://rostov.cian.ru/cat.php?deal_type=sale&district%5B0%5D=219&engine_version=2&offer_type=flat&p=1'
    URL_oktyabr = 'https://rostov.cian.ru/cat.php?deal_type=sale&district%5B0%5D=223&engine_version=2&offer_type=flat&p=1'
    MAX = 10
    parse_links(URL_vorosh)
    parse_links(URL_oktyabr)
    # data_ = get_page('https://www.cian.ru/sale/flat/289484529/')
    # if not isinstance(data_, tuple):
    #     data_ = final_fix(fix_data_after_parsing(data_))
    # print(data_['finishing'])
    # engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
    # data_.to_sql('float_float', engine, if_exists='append', index=False)
