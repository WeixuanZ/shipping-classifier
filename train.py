import json
import os
import uuid

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from datafetcher.date import date_generator


def fetch_data():
    """
    Crawl data using scrapy.
    """
    os.system("cd datafetcher && scrapy crawl port_spider -o ./cache/port_data.json")
    os.system("cd datafetcher && python3 vessel.py")
    os.system("cd datafetcher && python3 company.py")


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
    :param path: str
    :return data: dict
    """
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def concatenate(data):
    """
    Return all the names as a single list.
    :param data: dict
    :return combined_data: list
    """
    combined_data = []
    for i in data:
        combined_data += i["names"]
    return combined_data


def load_data(cache_dir):
    """
    Function for loading data.
    :param cache_dir: str
    :return port_data, vessel_data, company_data: list
    """
    port_data = concatenate(load_json(os.path.join(cache_dir, 'port_data.json')))
    vessel_data = load_json(os.path.join(cache_dir, 'vessel_data.json'))['names']
    company_data = load_json(os.path.join(cache_dir, 'company_data.json'))['names']
    return port_data, vessel_data, company_data


def rand_choose(data, num):
    """
    Function of random selection of subset.
    :param data: list
    :param num: int
    :return : list
    """
    return [data[i] for i in np.random.choice(np.arange(0, len(data), 1, dtype=np.int16), size=num)]


def generate_dataset(use_cache=True):
    """
    Function that combines the individual dataset.
    :param use_cache: bool [True]
    :return: dict
    """
    cache_dir = './datafetcher/cache'
    try:
        os.makedirs(cache_dir)
    except FileExistsError:
        pass

    if use_cache:
        try:
            port_data, vessel_data, company_data = load_data(cache_dir)
        except FileNotFoundError:
            fetch_data()
            port_data, vessel_data, company_data = load_data(cache_dir)
    else:
        fetch_data()
        port_data, vessel_data, company_data = load_data(cache_dir)

    return {'port': rand_choose(port_data, len(vessel_data)), 'date': date_generator(len(company_data)),
            'vessel': vessel_data, 'company': company_data}


def format_dataset(data):
    """
    Function that formats and store the dataset into required format.
    :param data: dict
    """
    identifier = []
    label = []
    text = []
    for k, v in data.items():
        for i in v:
            identifier.append(uuid.uuid4())
            label.append(k)
            text.append(i)

    df = pd.DataFrame({'guid': identifier,
                       'label': label,
                       'alpha': ['a'] * len(label),
                       'text': text})

    df_train, _df_test = train_test_split(df, test_size=0.1)
    df_dev, df_test_with_label = train_test_split(_df_test, test_size=0.2)
    df_test = pd.DataFrame({'guid': df_test_with_label['guid'], 'text': df_test_with_label['text']})

    df_train.to_csv('./bert/dataset/train.tsv', sep='\t', index=False, header=False)
    df_dev.to_csv('./bert/dataset/dev.tsv', sep='\t', index=False, header=False)

    df_test_with_label.to_csv('./bert/dataset/test_with_label.tsv', sep='\t', index=False, header=True)
    df_test.to_csv('./bert/dataset/test.tsv', sep='\t', index=False, header=True)


def train():
    """
    Function for training.
    :param batch_size: int [32]
    :param epochs: float [3.0]
    """
    if os.path.isfile('./bert/dataset/train.tsv') is False or os.path.isfile('./bert/dataset/test.tsv') is False:
        format_dataset(generate_dataset())
    if os.path.isdir('./bert/model') is False or len(os.listdir('./bert/model/')) == 0:
        raise RuntimeError('Pretrained model not found')

    os.system(
        "cd ./bert && python3 run_classifier.py --task_name=cola --do_train=true --do_eval=true --data_dir=./dataset --vocab_file=./model/vocab.txt --bert_config_file=./model/bert_config.json --init_checkpoint=./model/bert_model.ckpt --max_seq_length=64 --train_batch_size=32 --learning_rate=5e-5 --num_train_epochs=3.0 --output_dir=./bert_output/ --do_lower_case=true --save_checkpoints_steps 100")


def test():
    os.system(
        "cd ./bert && python3 run_classifier.py --task_name=cola --do_predict=true --data_dir=./dataset --vocab_file=./model/vocab.txt --bert_config_file=./model/bert_config.json --init_checkpoint=./bert_output/model.ckpt-190 --max_seq_length=64 --output_dir=./bert_output/")

    df_test = pd.read_csv('./bert/dataset/test.tsv', sep='\t')
    df_test_with_label = pd.read_csv('./bert/dataset/test_with_label.tsv', sep='\t')

    df_result = pd.read_csv('./bert/bert_output/test_results.tsv', sep='\t', header=None)

    df_map_result = pd.DataFrame({
        'text': df_test['text'],
        'label': df_test_with_label['label'],
        'prediction': [['port', 'date', 'vessel', 'company'][i] for i in df_result.idxmax(axis=1)]
    })

    print(df_map_result)


dataset = generate_dataset()
# print(dataset)
# dump_json(dataset, './dataset.json')


# format_dataset(dataset)

# train()

test()
