import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

from func.predict_models import get_data_from_link, predict_models_bs_catboost, predict_models_bs_liner

engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')


def get_floats(city: str, district=None, eng=engine):
    result = None
    with (eng.connect() as conn):
        if district is not None:
            stmt = text(f"""SELECT link, price, cntroom, typeofhousing, totalarea, livingarea, kitchenarea, ff.address, fa.width, fa.long, city,district
                            FROM float_float ff
                            JOIN float_addrescoord fa ON ff.address = fa.address
                            WHERE city = '{city}' and district = '{district}' """)
        else:
            stmt = text(f"""SELECT link, price, cntroom, typeofhousing, totalarea, livingarea, kitchenarea, ff.address, fa.width, fa.long, city,district
                            FROM float_float ff
                            JOIN float_addrescoord fa ON ff.address = fa.address
                            WHERE city = '{city}'""")
        result = conn.execute(stmt)
    # value = [x for x in result.query]
    # fixed_value = []
    # for val in value:
    #     fixed_value.append(tuple("Пусто" if value is None else value for value in val))
    return result.keys().keys, result.all()


def get_floats_rent(city: str, district: str, eng=engine):
    result = None
    with (eng.connect() as conn):
        stmt = text(f"""SELECT price, cntroom, totalarea, ffr.address, fa.width, fa.long
                        FROM float_floatrent ffr
                        JOIN float_addrescoord fa ON ffr.address = fa.address
                        WHERE city = '{city}' and district = '{district}' """)
        result = conn.execute(stmt)
    return result.keys().keys, result.all()


def get_mean_price(cntroom: int, w: float, l: float, totalarea: float, df_floats: pd.DataFrame) -> float:
    # Filter DataFrame to include only apartments with the same number of rooms
    filtered_df = df_floats[(df_floats['cntroom'] == cntroom) & (abs(df_floats['totalarea'] - totalarea) < 30)].copy(
        deep=True)

    # Calculate Euclidean distance from given coordinates (w, l) to each apartment
    distance = []
    for index in range(len(filtered_df)):
        # Получаем конкретную строку по индексу
        row = filtered_df.iloc[index]

        # Вычисляем расстояние и добавляем его в список
        dist = np.sqrt((row['width'] - w) ** 2 + (row['long'] - l) ** 2)
        distance.append(dist)
    filtered_df['distance'] = distance

    # Sort DataFrame by distance to find the nearest apartments
    nearest_apartments = filtered_df.sort_values(by='distance').head(3)

    # Calculate the mean price of the nearest apartments
    mean_price = nearest_apartments['price'].mean()

    if not np.isnan(mean_price):
        return int(mean_price)
    else:
        return mean_price


def knn_price(city: str, district: str):
    columns, rows = get_floats(city, district)
    df = pd.DataFrame(rows, columns=columns)
    columns, rows = get_floats_rent(city, district)
    price_rent = []
    mean_price = []
    df_rent = pd.DataFrame(rows, columns=columns)
    for index, row in df.iterrows():
        price_rent.append(
            get_mean_price(row['cntroom'], row['width'], row['long'], row['totalarea'], df_floats=df_rent))
        mean_price.append(get_mean_price(row['cntroom'], row['width'], row['long'], row['totalarea'], df_floats=df))
    df['rent_price'] = price_rent
    df['mean_price'] = mean_price
    return df


def payback(city: str, district: str, repair=0):
    def month_pb(price: int, rent_price: float, totalarea: float, repair, msk=False, new_f=False):
        if msk:
            if repair:
                price += totalarea * repair
            elif new_f:
                price += totalarea * 60_000
            else:
                price += totalarea * 15_000
        else:
            if repair:
                price += totalarea * repair
            elif new_f:
                price += totalarea * 10_000
            else:
                price += totalarea * 7_000
        m_samoz = price / (rent_price - rent_price * (6. / 100))
        m2_ip = price / (rent_price - rent_price * (4. / 100))
        return m_samoz, m2_ip, price

    def capitalisation(price: int, rent_price: float):
        return (rent_price * 12) / (price * 100)

    df = knn_price(city, district)

    pay_back_sm = []
    pay_back_ip = []
    total_price = []
    capitalisation_list = []

    msk = True if city == "Москва" else False
    for index, row in df.iterrows():
        new_f = False
        price_float = None
        if row['typeofhousing'] == "Новостройка":
            new_f = True

        sm, ip, price_float = month_pb(price=row['price'], rent_price=row['rent_price'],
                                       totalarea=row['totalarea'], repair=repair, new_f=new_f, msk=msk)
        pay_back_sm.append(sm)
        pay_back_ip.append(ip)
        total_price.append(price_float)
        capitalisation_list.append(capitalisation(price=price_float, rent_price=row['rent_price']))

    df['pay_back_sm'] = pay_back_sm
    df['pay_back_ip'] = pay_back_ip
    df['total_price'] = total_price
    df['capitalisation'] = capitalisation_list

    df['pay_back_sm'] = df['pay_back_sm'].fillna(-1)
    df['pay_back_ip'] = df['pay_back_ip'].fillna(-1)
    df['total_price'] = df['total_price'].fillna(-1)
    df['capitalisation'] = df['capitalisation'].fillna(-1,)

    df['pay_back_sm'] = df['pay_back_sm'].apply(lambda x: int(x))
    df['pay_back_ip'] = df['pay_back_ip'].apply(lambda x: int(x))
    df['total_price'] = df['total_price'].apply(lambda x: int(x))
    df['capitalisation'] = df['capitalisation'].apply(lambda x: round(x, 6))

    df['pay_back_sm'] = df['pay_back_sm'].replace(-1, 'Недостаточно информации')
    df['pay_back_ip'] = df['pay_back_ip'].replace(-1, 'Недостаточно информации')
    df['total_price'] = df['total_price'].replace(-1, 'Недостаточно информации')
    df['capitalisation'] = df['capitalisation'].replace(-1, 'Недостаточно информации')

    df_predict = get_data_from_link(df.link)
    df['catboost'] = round(predict_models_bs_catboost(df_predict)*df.totalarea)

    df.drop(columns=['width', 'long', 'city', 'district'], inplace=True)

    df.columns = ['Объявление', 'Цена продажи', 'Кол-во комнат',
                  'Тип квартиры', 'Общая площадь', 'Жилая площадь',
                  'Кухонная площадь', 'Адресс', 'Примерная цена для сдачи в аренду',
                  'Средняя стоимость по ближайшим квартирам',
                  'Окуп для самозанятого (кол-во месяцов)', 'Окуп для ИП (кол-во месяцов)',
                  'Стоимость с учетом ремонта', '% капитализации', 'catboost']
    print(df.columns)
    return df, city, district


def statistic_district(city: str):
    _, rows = get_floats(city)
    columns = ['Объявление',
               'Цена продажи',
               'Кол-во комнат',
               'Тип квартиры',
               'Общая плоащдь',
               'Жилая площадь',
               'Кухонная площадь',
               'Адресс',
               'Широта',
               'Долгота',
               'Город',
               'Район'
               ]
    df_st = pd.DataFrame(rows, columns=columns)
    grouped = df_st[df_st['Город'] == city].groupby(['Район', 'Кол-во комнат'])['Цена продажи'].describe()
    # grouped.plot(kind='box', legend=True)
    # plt.show()
    grouped['std'].fillna(0, inplace=True)
    grouped['std'] = grouped['std'].apply(lambda x: int(x))
    grouped['mean'] = grouped['mean'].apply(lambda x: int(x))
    grouped['count'] = grouped['count'].apply(lambda x: int(x))
    grouped.reset_index(inplace=True)
    grouped.rename(columns={'mean': 'Средняя цена', 'std': 'Стандартное отклонение',
                            'count': 'Кол-во недвижимости'}, inplace=True)

    return grouped.values, grouped.columns, city


if __name__ == '__main__':
    city, district = 'Москва', 'ЮВАО'
    # c, d, g = statistic_district(city)
    print(payback(city, district)[0])
