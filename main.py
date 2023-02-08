from io import BytesIO
import requests
from PIL import Image

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "http://static-maps.yandex.ru/1.x/"

longitude, latitude, delta = None, None, '0.005'

question = input()

if 'search' in question:

    toponym_to_find = input()

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        ...

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

    coordinates = toponym["Point"]["pos"]

    longitude, latitude = coordinates.split(' ')

elif 'open with cords' in question:

    longitude, latitude = input().split()
    delta = input()

else:
    ...


if not(longitude is None and latitude is None):

    image_type = input()

    map_type = {
        'terrain map': 'map',
        'satellite imagery': 'sat',
        'names of g-objects': 'skl',
        'cork layer': 'trf',
    }

    map_params = {
        'll': ','.join([longitude, latitude]),
        'spn': ','.join([delta, delta]),
        'l': ','.join([map_type[i] for i in image_type.split('+')]),
        'pt': f'{longitude},{latitude},flag',
    }

    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(response.content)).show()
