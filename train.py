import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import uuid

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
    vessel_data = load_json(os.path.join(cache_dir, 'vessel_data.json'))['names']
    company_data = load_json(os.path.join(cache_dir, 'company_data.json'))['names']
    return port_data, vessel_data, company_data


def generate_dataset(use_cache=True):
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
        # Fetch and dump to file
        fetch_data()
        port_data, vessel_data, company_data = load_data(cache_dir)

    return {'port': port_data, 'date': date_generator(len(company_data)), 'vessel': vessel_data, 'company': company_data}


def format_dataset(data):
    identifier = []
    label = []
    text = []
    for k, v in data.items():
        for i in v:
            identifier.append(uuid.uuid4())
            label.append(k)
            text.append(i)

    df = pd.DataFrame({'guide': identifier,
    'label':label,
    'alpha': ['a']*len(label),
    'text': text})

    df_train, _df_test = train_test_split(df, test_size=0.1)
    df_dev, df_test = train_test_split(_df_test, test_size=0.2)
    df_test = pd.DataFrame({'guide': _df_test['guide'], 'text': _df_test['text']})

    df_train.to_csv('./bert/dataset/train.tsv', sep='\t', index=False, header=False)
    df_dev.to_csv('./bert/dataset/dev.tsv', sep='\t', index=False, header=False)
    df_test.to_csv('./bert/dataset/test.tsv', sep='\t', index=False, header=True)



def train():
    if os.path.isfile('./bert/dataset/train.tsv') is False or os.path.isfile('./bert/dataset/test.tsv') is False:
        format_dataset(generate_dataset())
    if os.path.isdir('./bert/model') is False or len(os.listdir('./bert/model/'))==0:
        raise RuntimeError('Pretrained model not found')

    os.system("cd ./bert && python3 run_classifier.py --task_name=cola --do_train=true --do_eval=true --data_dir=./dataset --vocab_file=./model/vocab.txt --bert_config_file=./model/bert_config.json --init_checkpoint=./model/bert_model.ckpt --max_seq_length=64 --train_batch_size=2 --learning_rate=5e-5 --num_train_epochs=3.0 --output_dir=./bert_output/ --do_lower_case=true --save_checkpoints_steps 10000")








dataset = generate_dataset()
# print(dataset)
# dump_json(dataset, './dataset.json')

format_dataset(dataset)

train()



