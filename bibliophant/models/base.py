"""This module defines a base class for all classes which map to SQL tables,
i.e. for all modules in the models package.
It further defines a mixin class which specifies created_date and
modified_date fields. These two columns will be added to all tables.

The init_database function can be used to create all tables
for a new collection.
"""

__all__ = []


from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import DateTime
from sqlalchemy import func


class BaseMixin:
    @declared_attr
    def created_date(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def modified_date(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now())


ModelBase = declarative_base(cls=BaseMixin)


def init_database(engine: "sqlalchemy.engine.Engine"):
    """initialize all tables when starting a new collection"""
    ModelBase.metadata.create_all(engine)
