"""This script saves you a bit of time if you want to use bibliophant
from an interactive Python shell.

Run it:
ipython -i start_shell.py -- ~/path/to/your/collection
"""

import sys
import json

from bibliophant.session import resolve_root, start_engine, session_scope
from bibliophant.models import (
    Record,
    Author,
    Article,
    Journal,
    Eprint,
    Book,
    Publisher,
    Tag,
    Url,
)
from bibliophant.json_io import record_from_dict, store_record, load_record
from bibliophant.importers.crossref import doi_to_record
from bibliophant.importers.arxiv import arxiv_id_to_record, download_arxiv_eprint
from bibliophant.exporters.bibtex import (
    record_to_bibtex,
    records_to_bibfile,
    collection_to_bibfile,
)

from bibliophant.misc import *
from bibliophant.db_shortcuts import *


def print_json(json_obj):
    """print nicely formatted JSON"""
    print(json.dumps(json_obj, indent=4))


if __name__ == "__main__":
    root = resolve_root(sys.argv[-1])
    start_engine(root, create_db=True)
