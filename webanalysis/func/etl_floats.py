import pandas as pd
from sqlalchemy import create_engine, text


def get_floats():
    engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
    query = text(
        "SELECT ff.*, fa.width, fa.long FROM float_float as ff JOIN float_addrescoord as fa ON ff.address = fa.address")
    with (engine.connect() as conn):
        rslt = conn.execute(query)
        return rslt.all(), rslt.keys()


def func(data, col):
    pd.DataFrame(data, columns=col).to_csv('floats.csv', index=False)


if __name__ == '__main__':
    data, col = get_floats()
    func(data, col)
