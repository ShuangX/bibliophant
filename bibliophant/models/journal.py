"""This module defines a class Journal which stores information
about a journal in which an article was published.
It further defines functions to validate the type and format
of the class's data members.
"""

__all__ = []


from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import ModelBase
from ..misc import format_string


def validate_name(name: str) -> str:
    """validate the name field"""
    if not isinstance(name, str):
        raise ValueError("name must be a str")

    name = format_string(name)
    if len(name) < 4:
        raise ValueError("name must have at least 4 characters")

    return name


class Journal(ModelBase):
    """class for storing information about a journal"""

    __tablename__ = "journal"

    id = Column(Integer, primary_key=True)

    articles = relationship("Article", back_populates="_journal")

    _name = Column(String, nullable=False)

    def __init__(self, name: str):
        self._name = validate_name(name)

    def __repr__(self):
        return 'Journal("' + self._name + '")'

    def __str__(self):
        return self._name

    def to_dict(self):
        """Export all properties of the model which are not None as a dict.
        This is used for JSON serialization.
        """
        fields = [("name", self._name)]
        return {key: value for key, value in fields if value}

    @hybrid_property
    def name(self) -> str:
        """name of the journal"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = validate_name(value)
