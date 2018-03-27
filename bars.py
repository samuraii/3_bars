import json
import sys
import math


def get_data_from_file(path_to_file):
    try:
        with open(path_to_file) as file_data:
            return json.loads(file_data.read())['features']
    except (FileNotFoundError, IOError):
        print('Файл не найден.')


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
    except ValueError:
        print('Координаты должны быть числом, либо числом с плавающей точкой')
    else:
        return user_longitude, user_latitude


def get_bar_coordinates(bar_data):
    bar_longtitude = bar_data['geometry']['coordinates'][0]
    bar_latitude = bar_data['geometry']['coordinates'][1]
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
    
    bars_data = get_data_from_file(sys.argv[1])
    biggest_bar = get_biggest_bar(bars_data)
    smallest_bar = get_smallest_bar(bars_data)
    closest_bar = get_closest_bar(bars_data)

    print('Самый большой бар: {}'.format(get_bar_name(biggest_bar)))
    print('Самый маленький бар: {}'.format(get_bar_name(smallest_bar)))
    print('Самый близкий бар: {}'.format(get_bar_name(closest_bar)))
