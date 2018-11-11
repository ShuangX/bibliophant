"""This module defines a class Publisher which stores information
about the publisher of a book.
It further defines functions to validate the type and format
of the class's data members.
"""

__all__ = []

from typing import Optional

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


def validate_address(address: Optional[str]) -> Optional[str]:
    """validate the address field"""
    if address is None:
        return None

    if not isinstance(address, str):
        raise ValueError("address must be a str")

    address = format_string(address)
    if len(address) < 4:
        raise ValueError("address must have at least 4 characters")

    return address


class Publisher(ModelBase):
    """class for storing information about a book's publisher"""

    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True)

    books = relationship("Book", back_populates="_publisher")

    _name = Column(String, nullable=False)
    _address = Column(String)

    def __init__(self, name: str, address: Optional[str] = None):
        self._name = validate_name(name)
        self._address = validate_address(address)

    def __repr__(self):
        res = 'Publisher("' + self._name + '"'
        if self._address:
            res += ', "' + self._address + '"'
        res += ")"
        return res

    def __str__(self):
        if self._address:
            return self._name + ", " + self._address
        return self._name

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [("name", self._name), ("address", self._address)]
        dict_ = {}
        for key, value in fields:
            if value:
                dict_[key] = value
        return dict_

    @hybrid_property
    def name(self) -> str:
        """name of the publisher"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = validate_name(value)

    @hybrid_property
    def address(self) -> Optional[str]:
        """address of the publisher (usually only city)"""
        return self._address

    @address.setter
    def address(self, value: Optional[str]):
        self._address = validate_address(value)
