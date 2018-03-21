import json


with open('key') as f:
    key = f.read()


def load_data(feature):
    import urllib.request
    url = 'https://apidata.mos.ru/v1/features/{0}?api_key={1}'.format(feature, key)
    data = urllib.request.urlopen(url)
    return json.loads(data.read().decode('utf-8'))


def get_biggest_bar(data):
    pass


def get_smallest_bar(data):
    pass


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    print(load_data(1796)['features'][0])
