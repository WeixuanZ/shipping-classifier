import argparse
import os
import uuid

import pandas as pd

from train import test

parser = argparse.ArgumentParser(prog='main', usage='%(prog)s [-t] strings', description='Classifier.')

parser.add_argument('-t', '--text', type=str, nargs='+', default=[], required=False, help='Strings to be classified.')

args = parser.parse_args()

use_test = False if len(args.text) != 0 else True

if use_test is True:
    test()
else:
    try:
        os.makedirs('./bert/cache')
    except FileExistsError:
        pass
    identifier = []
    for i in args.text:
        identifier.append(uuid.uuid4())
    df = pd.DataFrame({'guid': identifier, 'text': args.text})
    df.to_csv('./bert/cache/test.tsv', sep='\t', index=False, header=True)

    os.system(
        "cd ./bert && python3 run_classifier.py --task_name=cola --do_predict=true --data_dir=./cache --vocab_file=./model/vocab.txt --bert_config_file=./model/bert_config.json --init_checkpoint=./bert_output/model.ckpt-190 --max_seq_length=64 --output_dir=./cache/")
    df_result = pd.read_csv('./bert/cache/test_results.tsv', sep='\t', header=None)
    df_map_result = pd.DataFrame({
        'text': df['text'],
        'prediction': [['port', 'date', 'vessel', 'company'][i] for i in df_result.idxmax(axis=1)]
    })
    print(df_map_result)
