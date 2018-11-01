"""this module is about reading and writing biblopgraphic records"""
__all__ = ['load_record', 'store_record']

import json
from pathlib import Path
from typing import Dict, Optional

from .schema.validate import validate_record


def load_record(root_folder: str, key: str) -> Dict:
    """Returns a dict (JSON object) for the record with the given key.
    root_folder can be a relative or absolute path.
    """
    record_file = Path(root_folder) / key / (key + '.json')
    if not record_file.is_file():
        raise Exception(f"the record file {record_file} does not exist")
    with record_file.open('r') as file:
        record = json.load(file)
    return record


def store_record(root_folder: str, record: Dict, overwrite: Optional[bool] = False):
    """Validates and stores a record."""
    validate_record(record)
    record_folder = Path(root_folder) / record['key']
    try:
        record_folder.mkdir(exist_ok=overwrite)
    except FileNotFoundError:
        raise Exception('the given root folder does not exist')
    except FileExistsError:
        raise Exception('the record folder already exists')
    record_file = record_folder / (record['key'] + '.json')
    with record_file.open('w') as file:
        json.dump(record, file, indent=4)
