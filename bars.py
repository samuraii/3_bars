import json
import sys
import math


def get_data_from_file(path_to_file):
    try:
        with open(path_to_file) as file_data:
            return json.loads(file_data.read())['features']
    except json.decoder.JSONDecodeError:
        return None


def get_bar_seats(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_bar_name(bar):
    return bar['properties']['Attributes']['Name']


def get_biggest_bar(bars_data):
    return max(bars_data, key=lambda bar: get_bar_seats(bar))


def get_smallest_bar(bars_data):
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
    try:
        bars_data = get_data_from_file(sys.argv[1])
    except IndexError:
        exit('Для корректной работы нужно передать скрипту файл.')
    except FileNotFoundError:
        exit('Не могу найти такой файл.')

    if bars_data:
        biggest_bar = get_biggest_bar(bars_data)
        smallest_bar = get_smallest_bar(bars_data)
        print('Самый большой бар: {}'.format(get_bar_name(biggest_bar)))
        print('Самый мелкий бар: {}'.format(get_bar_name(bars_data)))
        user_coordinates = get_user_coordinates()
        closest_bar = get_closest_bar(bars_data, user_coordinates)
        print('Самый близкий бар: {}'.format(get_bar_name(closest_bar)))
    else:
        exit('Содержимое файла не валидно, проверь что там.')
