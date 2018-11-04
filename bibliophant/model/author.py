"""This module defines a class Author.
It further defines functions to validate the type and format
of the class's data members."""

__all__ = []

import re
from typing import Optional


REGEX_PATTERNS = {"email": re.compile(r"^[^@]+@[^@]+\.[^@]+$")}


def validate_last(last: str) -> str:
    """validate the field for the author's last name"""
    if not (isinstance(last, str) and len(last) >= 2):
        raise ValueError("last must be a str with at least 2 characters")
    return last


def validate_first(first: Optional[str]) -> Optional[str]:
    """validate the field for the author's first name"""
    if first is not None and not (isinstance(first, str) and len(first) >= 2):
        raise ValueError("first must be a str with at least 2 characters")
    return first


def validate_email(email: Optional[str]) -> Optional[str]:
    """validate the field for the author's email address"""
    if email is not None and not (
        isinstance(email, str) and REGEX_PATTERNS["email"].search(email)
    ):
        raise ValueError(
            "email must be a str that matches " + REGEX_PATTERNS["email"].pattern
        )
    return email


class Author:
    """class for an author with last name
    and optionally first name and email address
    """

    __slots__ = ("__last", "__first", "__email")

    def __init__(
        self, last: str, first: Optional[str] = None, email: Optional[str] = None
    ):
        self.__last = validate_last(last)
        self.__first = validate_first(first)
        self.__email = validate_email(email)

    def __str__(self):
        if self.first:
            return self.__first + " " + self.last
        return self.__last

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [
            ("last", self.__last),
            ("first", self.__first),
            ("email", self.__email),
        ]
        dict_ = {}
        for key, value in fields:
            if value:
                dict_[key] = value
        return dict_

    @property
    def last(self) -> str:
        """the last name of the author"""
        return self.__last

    @last.setter
    def last(self, value: str):
        self.__last = validate_last(value)

    @property
    def first(self) -> Optional[str]:
        """the first name of the author"""
        return self.__first

    @first.setter
    def first(self, value: Optional[str]):
        self.__first = validate_first(value)

    @property
    def email(self) -> Optional[str]:
        """the email address of the author"""
        return self.__email

    @email.setter
    def email(self, value: Optional[str]):
        self.__email = validate_email(value)
