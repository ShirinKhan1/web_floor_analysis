# !pip install ymaps
from ymaps import Geocode
import requests

key = 'f237f550-e7ae-44ad-935a-d58367c3eaaa'
client = Geocode(key)

# geocode
codes = client.geocode('Москва, СЗАО, р-н Хорошево-Мневники, ул. Народного Ополчения, 15К1')

# print(codes)
print(codes['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'])
#
#
# # Координаты первой точки
# lat_lng1 = '37.474677,55.773348'
#
# # Координаты второй точки
# lat_lng2 = '37.473995,55.778011'

# Запрос к API Yandex Maps для расчета расстояния
# from math import radians, sin, cos, sqrt, atan2
#
# def haversine(lat1, lon1, lat2, lon2):
#     # Радиус Земли в километрах
#     R = 6371.0
#
#     # Преобразование координат в радианы
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#
#     # Разница между широтами и долготами
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#
#     # Формула гаверсинусов
#     a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#     # Расстояние между двумя точками
#     distance = R * c
#
#     return distance
#
# # Координаты первой точки
# lat1, lon1 = 55.773348, 37.474677
#
# # Координаты остальных точек
# points = [
#     {'lat': 55.778011, 'lon': 37.473995},
#     {'lat': 55.777000, 'lon': 37.476000},
#     {'lat': 55.771000, 'lon': 37.478000},
#     {'lat': 55.774000, 'lon': 37.480000}
# ]
#
# # Вычисление расстояния от первой точки до остальных точек
# distances = []
# for point in points:
#     distance = haversine(lat1, lon1, point['lat'], point['lon'])
#     distances.append(distance)
#
# # Находим индекс точки с минимальным расстоянием
# closest_index = distances.index(min(distances))
#
# # Получаем координаты и расстояние до ближайшей точки
# closest_point = points[closest_index]
# closest_distance = distances[closest_index]
#
# print("Ближайшая точка:", closest_point)
# print("Расстояние до ближайшей точки:", closest_distance, "километров")
