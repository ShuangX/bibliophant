"""This module defines a class Author.
It further defines functions to validate the type and format
of the class's data members."""

__all__ = []

import re
from typing import Optional

from sqlalchemy.sql.schema import Column, Table, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import ModelBase
from ..misc import format_string


REGEX_PATTERNS = {"email": re.compile(r"^[^@]+@[^@]+\.[^@]+$")}


def validate_last(last: str) -> str:
    """validate the field for the author's last name"""
    if not isinstance(last, str):
        raise ValueError("last must be a str")

    last = format_string(last)
    if len(last) < 2:
        raise ValueError("last must have at least 2 characters")

    return last


def validate_first(first: Optional[str]) -> Optional[str]:
    """validate the field for the author's first name"""
    if first is None:
        return None

    if not isinstance(first, str):
        raise ValueError("first must be a str")

    first = format_string(first)
    if len(first) < 2:
        raise ValueError("first must have at least 2 characters")

    return first


def validate_email(email: Optional[str]) -> Optional[str]:
    """validate the field for the author's email address"""
    if email is None:
        return None

    # TODO check for unallowed chars in email, use format_string?
    if not (isinstance(email, str) and REGEX_PATTERNS["email"].search(email)):
        raise ValueError(
            "email must be a str that matches " + REGEX_PATTERNS["email"].pattern
        )

    return email


author_association_table = Table(
    "author_association",
    ModelBase.metadata,
    Column("author_id", Integer, ForeignKey("author.id")),
    Column("record_id", Integer, ForeignKey("record.id")),
)


class Author(ModelBase):
    """class for an author with last name
    and optionally first name and email address
    """

    __tablename__ = "author"

    id = Column(Integer, primary_key=True)

    _last = Column(String, nullable=False)
    _first = Column(String)
    _email = Column(String)

    records = relationship(
        "Record", secondary=author_association_table, back_populates="_authors"
    )

    def __init__(
        self, last: str, first: Optional[str] = None, email: Optional[str] = None
    ):
        self._last = validate_last(last)
        self._first = validate_first(first)
        self._email = validate_email(email)

    def __repr__(self):
        res = 'Author("' + self._last + '"'
        if self._first:
            res += ', first="' + self._first + '"'
        if self._email:
            res += ', email="' + self._email + '"'
        res += ")"
        return res

    def __str__(self):
        if self.first:
            return self._last + ", " + self._first
        return self._last

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [("last", self._last), ("first", self._first), ("email", self._email)]
        dict_ = {}
        for key, value in fields:
            if value:
                dict_[key] = value
        return dict_

    @hybrid_property
    def last(self) -> str:
        """the last name of the author"""
        return self._last

    @last.setter
    def last(self, value: str):
        self._last = validate_last(value)

    @hybrid_property
    def first(self) -> Optional[str]:
        """the first name of the author"""
        return self._first

    @first.setter
    def first(self, value: Optional[str]):
        self._first = validate_first(value)

    @hybrid_property
    def email(self) -> Optional[str]:
        """the email address of the author"""
        return self._email

    @email.setter
    def email(self, value: Optional[str]):
        self._email = validate_email(value)
