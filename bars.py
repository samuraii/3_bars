import json
import requests
import os
import math


def load_data():

    if not os.path.isfile('data'):
        try:
            with open('key') as f:
                api_key = f.read()
            api_key_param = {'api_key': api_key}
            data_url = 'https://apidata.mos.ru/v1/features/1796'
            data_from_url = requests.get(data_url, params=api_key_param)
            with open('data', 'w+') as f:
                f.write(data_from_url.text)
            print('Данные успешно получены из ' + data_url)
        except requests.exceptions.HTTPError:
            print('Ошибка при получении данных из ' + data_url)
            return

    with open('data', 'r') as f:
        bar_data = json.loads(f.read())['features']
        return bar_data


def get_bar_seats(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_bar_name(bar):
    return bar['properties']['Attributes']['Name']


def get_bar_address(bar):
    return bar['properties']['Attributes']['Address']


def extremum_getter(bar_data, extremum_func):
    bar_size = extremum_func(
        bar_data,
        key=lambda bar: get_bar_seats(bar)
    )
    return bar_size


def get_closest_bar(bar_data):

    try:
        user_latitude = float(input('Введите вашу широту: '))
        user_longitude = float(input('Введите вашу долготу: '))
    except ValueError:
        print('Координаты должны быть числом с плавающей точкой')

    closest_bar = bar_data[0]
    previous_distance = None

    for bar in bar_data:
        bar_longtitude = float(bar['geometry']['coordinates'][0])
        bar_latitude = float(bar['geometry']['coordinates'][1])
        sqr_latitude = (bar_latitude - user_latitude) ** 2
        sqr_longtitude = (bar_longtitude - user_longitude) ** 2
        distance = math.sqrt(sqr_latitude + sqr_longtitude)

        if previous_distance:
            if distance < previous_distance:
                closest_bar = bar

        previous_distance = distance

    return closest_bar


if __name__ == '__main__':
    bar_data = load_data()
    biggest_bar = extremum_getter(bar_data, max)
    print('Самый большой бар называется: ' + get_bar_name(biggest_bar))
    print('Находится по адресу: ' + get_bar_address(biggest_bar))
    print('------------------------------------------------------------')
    smallest_bar = extremum_getter(bar_data, min)
    print('Самый маленький бар называется: ' + get_bar_name(smallest_bar))
    print('Находится по адресу: ' + get_bar_address(smallest_bar))
    print('------------------------------------------------------------')
    closest_bar = get_closest_bar(bar_data)
    print('Самый близкий бар называется: ' + get_bar_name(closest_bar))
    print('Находится по адресу: ' + get_bar_address(closest_bar))
