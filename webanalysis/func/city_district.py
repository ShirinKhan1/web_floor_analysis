import pandas as pd
from sqlalchemy import create_engine, text


def get_adress():
    engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')
    with (engine.connect() as conn):
        query = text(
            "SELECT DISTINCT address FROM float_float WHERE address not in (SELECT address FROM float_addrescoord)")
        return conn.execute(query).all()


def append_to_sql(addres: str):
    engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')

