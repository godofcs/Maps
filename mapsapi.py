import requests
import os
import pprint
from io import BytesIO
from PIL import Image


adres = "https://geocode-maps.yandex.ru/1.x/"
params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": "Владивосток",
    "format": "json"
}
resque = requests.get(adres, params=params).json()
obect = resque["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
obect_coord = obect["Point"]["pos"]
adres2 = "https://static-maps.yandex.ru/1.x/"
params2 = {
    "l": "sat",
    "ll": ",".join(obect_coord.split()),
    "spn": "1,1"
}
resque2 = requests.get(adres2, params=params2)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(resque2.content)

os.remove(map_file)
# первая задача