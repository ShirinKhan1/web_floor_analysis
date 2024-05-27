import time

import pandas as pd
from sqlalchemy import create_engine, text
from ymaps import Geocode
import json


def geocode(addres: str):
    key = None
    with open('key_ya.json', 'r') as key:
        key = json.load(key)['key']
    client = Geocode(key)
    codes = client.geocode(addres)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    return codes.split(' ')


def append_to_sql(addres: str):
    engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
    # data.to_sql('float_float', engine, if_exists='append', index=False)
    x_y = geocode(addres)
    x_y.append(addres)
    print(x_y)
    data = {
        'width': [float(x_y[1])],
        'long': [float(x_y[0])],
        'address': [x_y[2]]
    }
    (pd.DataFrame(data).
     to_sql('float_addrescoord', engine, if_exists='append', index=False))


def get_adress(rent=False):
    engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
    with (engine.connect() as conn):
        query = None
        if rent:
            query = text(
                "SELECT DISTINCT address FROM float_floatrent WHERE address not in (SELECT address FROM float_addrescoord) LIMIT 1000")
        else:
            query = text(
                "SELECT DISTINCT address FROM float_float WHERE address not in (SELECT address FROM float_addrescoord) LIMIT 1000")
        return conn.execute(query).all()


if __name__ == '__main__':
    address = get_adress()
    for val in address:
        try:
            append_to_sql(val[0])
        except Exception as e:
            print(e, val[0])
        finally:
            # time.sleep(1)
            pass
