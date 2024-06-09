import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
import plotly.io as pio

engine = create_engine('postgresql://webanalysis:ramisdstu@localhost/webanalysis')


def get_geopandas():
    stmt = text(f"""SELECT price, fa.width, fa.long
                                FROM float_float ff
                                JOIN float_addrescoord fa ON ff.address = fa.address""")
    with (engine.connect() as conn):
        result = conn.execute(stmt)
        k = result.keys()
    col, rows = k, result.all()
    df = pd.DataFrame(rows, columns=col)
    geometry = [Point(xy) for xy in zip(df['long'], df['width'])]

    # Преобразование DataFrame в GeoDataFrame
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)
    geo_df.set_crs(epsg=4326, inplace=True)

    # Визуализация данных на карте с использованием Plotly
    fig = px.scatter_mapbox(geo_df,
                            lat=geo_df.geometry.y,
                            lon=geo_df.geometry.x,
                            size_max=30
                            ,
                            zoom=8.5,
                            center={"lat": 55.755613, "lon": 37.621979},
                            mapbox_style="open-street-map")
    return pio.to_html(fig, full_html=False)
