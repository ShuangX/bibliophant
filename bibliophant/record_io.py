"""this module is about reading and writing biblopgraphic records"""
__all__ = ['resolve_root', 'load_record', 'store_record']

import json
from pathlib import Path
from typing import Dict, Optional

from .schema.validate import validate_record


def resolve_root(root_folder: str) -> Path:
    """Resolves the root folder of a collection.
    Raises FileNotFoundError if the root_folder cannot be resolved.
    """
    try:
        resolved_root = Path(root_folder).resolve(strict=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"the collection's root folder {root_folder} could not be resolved.")
    return resolved_root


def load_record(root_folder: Path, key: str) -> Dict:
    """Returns a dict (JSON object) for the record with the given key.
    Raises FileNotFoundError if the record file does not exist.
    """
    record_file = root_folder / key / (key + '.json')
    try:
        with record_file.open('r') as file:
            record = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f'the record file {record_file} was not found')

    return record


def store_record(root_folder: Path,
                 record: Dict,
                 overwrite: Optional[bool] = False,
                 validate: Optional[bool] = True):
    """Stores a record.
    Raises FileExistsError if the record already exists and overwrite is False.
    """
    if validate:
        validate_record(record)

    record_folder = root_folder / record['key']

    try:
        record_folder.mkdir(exist_ok=overwrite)
    except FileExistsError:
        raise FileExistsError(f'the record folder {record_folder} already exists')

    record_file = record_folder / (record['key'] + '.json')
    with record_file.open('w') as file:
        json.dump(record, file, indent=4)
