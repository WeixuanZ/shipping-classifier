import json
import os

from datafetcher.date import date_generator


def fetch_data():
    """
    Crawl data using scrapy.
    """
    os.system("cd datafetcher && scrapy crawl port_spider -o ./cache/port_data.json")


def dump_json(data, path):
    """
    Save JSON object to file.
    :param data:
    :param filename:
    :return:
    """
    with open(path, 'w') as f:
        data = json.dump(data, f)
    return data


def load_json(path):
    """
    Load JSON object from file.
    :param path:
    :return:
    """
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def concatenate(data):
    """
    Return all the names as a single list.
    :param data:
    :return:
    """
    combined_data = []
    for i in data:
        combined_data += i["names"]
    return combined_data


def load_data(cache_dir):
    port_data = concatenate(load_json(os.path.join(cache_dir, 'port_data.json')))
    # vessel_data = concatenate(load_json(os.path.join(cache_dir, 'vessel_data.json')))
    # company_data = concatenate(load_json(os.path.join(cache_dir, 'company_data.json')))
    return port_data


def generate_dataset(use_cache=True):
    cache_dir = './datafetcher/cache'
    try:
        os.makedirs(cache_dir)
    except FileExistsError:
        pass

    if use_cache:
        try:
            port_data = load_data(cache_dir)
        except FileNotFoundError:
            fetch_data()
            port_data = load_data(cache_dir)
    else:
        # Fetch and dump to file
        fetch_data()
        port_data = load_data(cache_dir)

    return {'port': port_data, 'date': date_generator(1000)}


dataset = generate_dataset()
print(dataset)
