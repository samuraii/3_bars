import json
import requests
import os
import math


def get_user_api_key():
    try:
        with open('api_key') as file_with_key:
            api_key = file_with_key.read().strip()
        return {'api_key': api_key}
    except (FileNotFoundError, IOError):
        print('Отсутствует файл api_key в корневой папке')


def fetch_data_from_api(api_url, api_key):
    try:
        return requests.get(api_url, params=api_key)
    except requests.exceptions.HTTPError:
        print('Ошибка получения данных')


def create_bar_data_file(data_to_write):
    with open('bar_data.json', 'w+') as data_file:
        data_file.write(data_to_write.text)


def get_bar_seats(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_bar_name(bar):
    return bar['properties']['Attributes']['Name']


def get_bar_address(bar):
    return bar['properties']['Attributes']['Address']


def load_bar_data():
    with open('bar_data.json', 'r') as bars_data:
        return json.loads(bars_data.read())['features']


def get_biggest_bar(bars_data):
    return max(bars_data, key=lambda bar: get_bar_seats(bar))


def get_smallest_bar(bars_data):
    return min(bars_data, key=lambda bar: get_bar_seats(bar))


def get_user_coordinates():
    try:
        user_latitude = float(input('Введите вашу широту: '))
        user_longitude = float(input('Введите вашу долготу: '))
    except ValueError:
        print('Координаты должны быть числом, либо числом с плавающей точкой')
    else:
        return user_longitude, user_latitude


def get_bar_coordinates(bar_data):
    bar_longtitude = float(bar_data['geometry']['coordinates'][0])
    bar_latitude = float(bar_data['geometry']['coordinates'][1])
    return bar_longtitude, bar_latitude


def calculate_distance(user_coordinates, bar_coordinates):
    sqr_latitude = (bar_coordinates[0] - user_coordinates[0]) ** 2
    sqr_longtitude = (bar_coordinates[1] - user_coordinates[1]) ** 2
    distance = math.sqrt(sqr_latitude + sqr_longtitude)
    return distance


def get_closest_bar(bars_data):
    user_coordinates = get_user_coordinates()
    return min(
                bars_data, 
                key=lambda bar_data: calculate_distance(
                                user_coordinates, 
                                get_bar_coordinates(bar_data)
                )
    )


if __name__ == '__main__':
    
    if not os.path.isfile('bar_data.json'):
        api_url = 'https://apidata.mos.ru/v1/features/1796'
        api_key = get_user_api_key()
        data_from_url = fetch_data_from_api(api_url, api_key)
        create_bar_data_file(data_from_url)

    bars_data = load_bar_data()
    biggest_bar = get_biggest_bar(bars_data)
    smallest_bar = get_smallest_bar(bars_data)
    closest_bar = get_closest_bar(bars_data)

    print('Самый большой бар: {}'.format(get_bar_name(biggest_bar)))
    print('Самый маленький бар: {}'.format(get_bar_name(smallest_bar)))
    print('Самый близкий бар: {}'.format(get_bar_name(closest_bar)))
