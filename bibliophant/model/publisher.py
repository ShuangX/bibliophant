"""This module defines a class Publisher which stores information
about the publisher of a book.
It further defines functions to validate the type and format
of the class's data members.
"""

__all__ = []

from typing import Optional


def validate_name(name: str) -> str:
    """validate the name field"""
    if not (isinstance(name, str) and len(name) >= 4):
        raise ValueError("name must be a str with at least 4 characters")
    return name


def validate_address(address: Optional[str]) -> Optional[str]:
    """validate the address field"""
    if address is not None and not (isinstance(address, str) and len(address) >= 4):
        raise ValueError("address must be a str with at least 4 characters")
    return address


class Publisher:
    """class for storing information about a book's publisher"""

    __slots__ = ("__name", "__address")

    def __init__(self, name: str, address: Optional[str]):
        self.__name = validate_name(name)
        self.__address = validate_address(address)

    def __str__(self):
        if self.__address:
            return self.__name + ", " + self.__address
        return self.__name

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [("name", self.__name), ("address", self.__address)]
        dict_ = {}
        for key, value in fields:
            if value:
                dict_[key] = value
        return dict_

    @property
    def name(self) -> str:
        """name of the publisher"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = validate_name(value)

    @property
    def address(self) -> Optional[str]:
        """address of the publisher (usually only city)"""
        return self.__address

    @address.setter
    def address(self, value: Optional[str]):
        self.__address = validate_address(value)
