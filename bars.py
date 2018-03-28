import json
import sys
import math


def get_data_from_file(path_to_file):
    try:
        with open(path_to_file) as file_data:
            return json.loads(file_data.read())['features']
    except (FileNotFoundError, IOError, json.decoder.JSONDecodeError):
        return None


def get_bar_seats(bar):
    if bar is None:
        return 'Ошибка в данных'
    return bar['properties']['Attributes']['SeatsCount']


def get_bar_name(bar):
    if bar is None:
        return 'Ошибка в данных'
    return bar['properties']['Attributes']['Name']


def get_biggest_bar(bars_data):
    if bars_data is None:
        return 'Проблема с данными. Неверный формат.'
    else:
        return max(bars_data, key=lambda bar: get_bar_seats(bar))


def get_smallest_bar(bars_data):
    if bars_data is None:
        return 'Проблема с данными. Неверный формат.'
    else:
        return min(bars_data, key=lambda bar: get_bar_seats(bar))


def get_user_coordinates():
    try:
        user_latitude = float(input('Введите вашу широту: '))
        user_longitude = float(input('Введите вашу долготу: '))
        return user_longitude, user_latitude
    except ValueError:
        return None


def get_bar_coordinates(bar_data):
    return bar_data['geometry']['coordinates']


def calculate_distance(user_coordinates, bar_coordinates):
    sqr_latitude = (bar_coordinates[0] - user_coordinates[0]) ** 2
    sqr_longtitude = (bar_coordinates[1] - user_coordinates[1]) ** 2
    distance = math.sqrt(sqr_latitude + sqr_longtitude)
    return distance


def get_closest_bar(bars_data, user_coordinates):
    if bars_data is None or user_coordinates is None:
        return None

    return min(
        bars_data,
        key=lambda bar_data: calculate_distance(
            user_coordinates,
            get_bar_coordinates(bar_data)
        )
    )


if __name__ == '__main__':
    bars_data = get_data_from_file(sys.argv[1])
    if bars_data is None:
        print('Ошибка чтения файла с данными')
    else:
        biggest_bar = get_biggest_bar(bars_data)
        smallest_bar = get_smallest_bar(bars_data)
        print('Самый большой бар: {}'.format(get_bar_name(biggest_bar)))
        print('Самый маленький бар: {}'.format(get_bar_name(smallest_bar)))
        user_coordinates = get_user_coordinates()
        if user_coordinates is None:
            print('Координаты должны быть вещественными числами.')
        else:
            closest_bar = get_closest_bar(bars_data, user_coordinates)
            print('Самый близкий бар: {}'.format(get_bar_name(closest_bar)))
