"""This module defines a class Tag.
It further defines functions to validate the type and format
of the class's data members."""

__all__ = []

import re
from typing import Optional


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


class Tag:
    """class for a tag (with optional color code)"""

    __slots__ = ("__name", "__color")

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

    @property
    def name(self) -> str:
        """the name of tag"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = validate_name(value)

    @property
    def color(self) -> Optional[str]:
        """the color code of the tag (capitalized hex code)"""
        return self.__color

    @color.setter
    def color(self, value: Optional[str]):
        self.__color = validate_color(value)
