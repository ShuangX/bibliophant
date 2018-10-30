"""this module is about adding new biblopgraphic records"""

import os
import json

from bibliophant.schema.validate import validate_record

ROOT = '../records'


def key_generator(year, authors):
    """adds a key to the record"""
    key = str(year)
    for author in authors:
        key += author['last']
    return key.replace(' ', '')


def store_record(record, overwrite=False):
    """validates and stores a record"""
    validate_record(record)
    record_folder = os.path.join(ROOT, record['key'])
    if os.path.exists(record_folder):
        if not overwrite:
            raise Exception('the record already exists')
    else:
        os.makedirs(record_folder)
    record_file = os.path.join(record_folder, record['key'] + '.json')
    with open(record_file, 'w') as fp:
        json.dump(record, fp, indent=4)
