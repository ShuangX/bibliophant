"""This package contains the data model for bibliohoant.
The ORM sqlalchemy is used to link the model with a SQLite database.
"""


"""a context manager for using the database
"""
from .base import db


"""the following modules contain one class each,
that maps to a database table
"""
from . import author
from . import article, eprint
from . import book, publisher
from . import tag
from . import url


from . import json_io
