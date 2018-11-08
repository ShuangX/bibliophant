"""This module defines a class Url.
It further defines functions to validate the type and format
of the class's data members."""

__all__ = []

import re
from typing import Optional

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import ModelBase


REGEX_PATTERNS = {
    "uri": re.compile(r"^\w+:(\/?\/?)[^\s]+$"),
    "url": re.compile("""^(https?|ftp)://"""),
}


def validate_url(url: str) -> str:
    """validate the URL field"""
    if not (
        isinstance(url, str)
        and REGEX_PATTERNS["uri"].search(url)
        and REGEX_PATTERNS["url"].search(url)
    ):
        raise ValueError(
            "url must be a str that matches " + REGEX_PATTERNS["url"].pattern
        )
    return url


def validate_description(description: Optional[str]) -> Optional[str]:
    """validate the description field of the URL"""
    if description is not None and not (
        isinstance(description, str) and len(description) >= 3
    ):
        raise ValueError("description must be a str with at least 3 characters")
    return description


class Url(ModelBase):
    """class for a URL and an optional description of the hyperlink"""

    __tablename__ = "url"

    id = Column(Integer, primary_key=True)

    record_id = Column(Integer, ForeignKey("record.id"))
    record = relationship("Record", back_populates="_urls")

    _url = Column(String, nullable=False)
    _description = Column(String)

    def __init__(self, url: str, description: Optional[str] = None):
        self._url = validate_url(url)
        self._description = validate_description(description)

    def __str__(self):
        return self._url

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [("url", self.__url), ("description", self.__description)]
        dict_ = {}
        for key, value in fields:
            if value:
                dict_[key] = value
        return dict_

    @hybrid_property
    def url(self) -> str:
        """the hyperlink"""
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = validate_url(value)

    @hybrid_property
    def description(self) -> Optional[str]:
        """short description of the URL"""
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        self._description = validate_description(value)
