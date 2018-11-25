"""This module contains functions for exporting records to json files
and for recreating records from such files.
"""

__all__ = ["record_from_dict", "load_record", "store_record"]


from pathlib import Path
import json
from typing import Optional, Dict

from .models.author import Author
from .models.record import Record


def record_from_dict(record_dict: Dict) -> Record:
    """Returns an Article or a Book given the corresponding dict."""
    record = record_dict.copy()

    try:
        type_ = record.pop("type")
    except KeyError:
        raise ValueError("record_dict must have a key 'type'")

    if type_ == "article":
        from .models.article import Article as RecordClass
    elif type_ == "book":
        from .models.book import Book as RecordClass
    else:
        raise ValueError("record_dict['type'] must be 'book' or 'article'")

    record["authors"] = [Author(**e) for e in record["authors"]]

    if "journal" in record:
        from .models.journal import Journal

        record["journal"] = Journal(**record["journal"])

    if "eprint" in record:
        from .models.eprint import Eprint

        record["eprint"] = Eprint(**record["eprint"])

    if "publisher" in record:
        from .models.publisher import Publisher

        record["publisher"] = Publisher(**record["publisher"])

    if "urls" in record:
        from .models.url import Url

        record["urls"] = [Url(**e) for e in record["urls"]]

    if "tags" in record:
        from .models.tag import Tag

        record["tags"] = [Tag(**e) for e in record["tags"]]

    record = RecordClass(**record)

    return record


def load_record(path: Path) -> Record:
    """Imports an Article or a Book from a JSON file.
    Path can either point to the record folder
    or directly to the JSON file.
    Raises FileNotFoundError if the JSON file does not exist.
    """
    path = Path(path)
    if path.is_dir():
        path = path / (path.name + ".json")
    try:
        with path.open("r") as file:
            record = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"the record file {path} was not found")

    return record_from_dict(record)


def store_record(record: Record, root_folder: Path, overwrite: Optional[bool] = False):
    """Creates record folder and exports a record to the JSON file
    <root_folder>/<record.key>/<record.key>.json.
    Raises FileExistsError if the record already exists and overwrite is False.
    """
    record_folder = root_folder / record.key

    try:
        record_folder.mkdir(exist_ok=overwrite)
    except FileExistsError:
        raise FileExistsError(f"the record folder {record_folder} already exists")

    record_file = record_folder / (record.key + ".json")
    with record_file.open("w") as file:
        json.dump(record.to_dict(), file, indent=4)
