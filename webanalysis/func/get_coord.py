import pandas as pd
from sqlalchemy import create_engine
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
    df = pd.DataFrame(data)
    (pd.DataFrame(data).
     to_sql('float_addrescoord', engine, if_exists='append', index=False))


if __name__ == '__main__':
    append_to_sql(
        "Москва СЗАО р-н Покровское-Стрешнево Северо-Западный административный округ Холланд Парк жилой комплекс к8")
