"""This module defines a class Tag.
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


REGEX_PATTERNS = {"color": re.compile("""^[0-9A-F]{6}$""")}


def validate_name(name: str) -> str:
    """validate the tag's name field"""
    if not (isinstance(name, str) and len(name) >= 2):
        raise ValueError("name must be a str with at least 2 characters")
    return name


def validate_color(color: Optional[str]) -> Optional[str]:
    """validate the tag's color field"""
    if color is not None and not (
        isinstance(color, str) and REGEX_PATTERNS["color"].search(color)
    ):
        raise ValueError("color must match " + REGEX_PATTERNS["color"].pattern)
    return color


tag_association_table = Table(
    "tag_association",
    ModelBase.metadata,
    Column("tag_id", Integer, ForeignKey("tag.id")),
    Column("record_id", Integer, ForeignKey("record.id")),
)


class Tag(ModelBase):
    """class for a tag (with optional color code)"""

    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)

    __name = Column(String, nullable=False)
    __color = Column(String)

    records = relationship(
        "Record", secondary=tag_association_table, back_populates="__tags"
    )

    def __init__(self, name: str, color: Optional[str] = None):
        self.__name = validate_name(name)
        self.__color = validate_color(color)

    def __str__(self):
        return self.__name

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [("name", self.__name), ("color", self.__color)]
        dict_ = {}
        for key, value in fields:
            if value:
                dict_[key] = value
        return dict_

    @hybrid_property
    def name(self) -> str:
        """the name of tag"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = validate_name(value)

    @hybrid_property
    def color(self) -> Optional[str]:
        """the color code of the tag (capitalized hex code)"""
        return self.__color

    @color.setter
    def color(self, value: Optional[str]):
        self.__color = validate_color(value)
