"""This module defines a base class for all classes which map to SQL tables,
i.e. for all modules in the models package.
It further defines a mixin class which specifies created_date and
modified_date fields. These two columns will be added to all tables.

The init_database function can be used to create all tables
for a new collection.
"""

__all__ = []


from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.declarative import declared_attr, declarative_base, DeclarativeMeta
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import DateTime
from sqlalchemy import func


class BaseMixin(metaclass=ABCMeta):
    @declared_attr
    def created_date(cls):
        """a column which saves the date of creation of the data"""
        return Column(DateTime, default=func.now())

    @declared_attr
    def modified_date(cls):
        """a column which saves the date of last modification of the data"""
        return Column(DateTime, default=func.now(), onupdate=func.now())

    @abstractmethod
    def __repr__(self):
        """All models should have a nice representation
        when bibliophant is used with the Python REPL.
        """
        pass

    @abstractmethod
    def __str__(self):
        """All models should have a short string representation."""
        pass

    @abstractmethod
    def to_dict(self):
        """Export all properties of the model which are not None as a dict.
        This is used for JSON serialization.
        """
        pass


class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    """abstract base class for all models"""

    pass


ModelBase = declarative_base(cls=BaseMixin, metaclass=DeclarativeABCMeta)


def init_database(engine: "sqlalchemy.engine.Engine"):
    """Initialize all tables when starting a new collection"""
    ModelBase.metadata.create_all(engine)
