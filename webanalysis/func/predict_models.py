from sklearn.preprocessing import LabelEncoder
import pandas as pd
from catboost import CatBoostRegressor, Pool
from sqlalchemy import create_engine, text
import pickle

engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')


def predict_models_bs_catboost(data: pd.DataFrame):
    BEST_FEATURE = ['totalarea', 'cntroom', 'district', 'long', 'ceiling', 'kitchenarea', 'width', 'maxfloor',
                    'livingarea']
    data = data[BEST_FEATURE]
    model = CatBoostRegressor().load_model('func/top_fet_catboost')
    return [int(x) for x in model.predict(data)]


def get_data_from_link(links: list):
    links = [f"'{element}'" for element in links]
    l = ', '.join(links)
    qry = f"""SELECT ff.*, fa.width, fa.long
                        FROM float_float ff
                        JOIN float_addrescoord fa ON ff.address = fa.address
                        where link in ({l})"""
    df = pd.read_sql_query(qry, engine)
    return df


def predict_models_bs_liner(data: pd.DataFrame):
    BEST_FEATURE = ['totalarea', 'cntroom', 'district', 'long', 'ceiling', 'kitchenarea', 'width', 'maxfloor',
                    'livingarea']
    data = data[BEST_FEATURE]
    ceiling = 3.03452713682158
    kitchenarea = {0: 5.741776,
                   1: 11.714002,
                   2: 12.645207,
                   3: 18.119613,
                   4: 19.729673,
                   5: 22.580870}

    livingarea = {0: 13.866038,
                  1: 17.308859,
                  2: 30.701434,
                  3: 61.037017,
                  4: 79.482310,
                  5: 114.412150}

    for i in range(6):
        data.loc[data['cntroom'] == i, 'kitchenarea'] = data.loc[data['cntroom'] == i, 'kitchenarea'].fillna(
            kitchenarea[i])
        data.loc[data['cntroom'] == i, 'livingarea'] = data.loc[data['cntroom'] == i, 'livingarea'].fillna(
            livingarea[i])

    data['ceiling'] = data['ceiling'].fillna(ceiling)

    data = pd.get_dummies(data, columns=['district', 'cntroom'])
    filename = 'GradientBoostingRegressor.pkl'
    model = pickle.load(open(filename, 'rb'))
    return [int(x) for x in model.predict(data)]
    # return model.predict(data)

if __name__ == '__main__':
    test_qry = f"""SELECT link from float_float where city = 'Москва'"""
    test_links = pd.read_sql_query(test_qry, engine).link.tolist()
    predict_models_bs_catboost(get_data_from_link(test_links))
    predict_models_bs_liner(get_data_from_link(test_links))
