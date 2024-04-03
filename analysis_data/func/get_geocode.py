# !pip install ymaps
from ymaps import Geocode
key = ''
client = Geocode(key)

# geocode
codes = client.geocode('Москва, СЗАО, р-н Хорошево-Мневники, ул. Народного Ополчения, 15К1')

# print(codes)
print(codes['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'])