"""This module defines a class Eprint which stores a reference
to an eprint on a site such as the arXiv.
It further defines functions to validate the type and format
of the class's data members.
"""

__all__ = []

from typing import Optional


def validate_eprint(eprint: str) -> str:
    """validate the eprint field"""
    if not (isinstance(eprint, str) and len(eprint) >= 9):
        raise ValueError("eprint must be a str with at least 9 characters")
    return eprint


def validate_archive_prefix(
    eprint: str, archive_prefix: Optional[str]
) -> Optional[str]:
    """validate the archive_prefix field
    based on the content of the eprint field
    """
    # old style identifiers don't require the field
    if "/" in eprint and archive_prefix is not None:
        raise ValueError("this field is not required for old-style identifiers")
    # new style identifiers do require it
    if "/" not in eprint and not (
        isinstance(archive_prefix, str) and len(archive_prefix) >= 5
    ):
        raise ValueError("archive_prefix must be a str with at least 5 characters")
    return archive_prefix


def validate_primary_class(eprint: str, primary_class: Optional[str]) -> Optional[str]:
    """validate the primary_class field
    based on the content of the eprint field
    """
    # old style identifiers don't require the field
    if "/" in eprint and primary_class is not None:
        raise ValueError("this field is not required for old-style identifiers")
    # new style identifiers do require it
    if "/" not in eprint and not (
        isinstance(primary_class, str) and len(primary_class) >= 5
    ):
        raise ValueError("primary_class must be a str with at least 5 characters")
    return primary_class


class Eprint:
    """class for referring to (arXiv) eprints
    For further information go to:
    https://arxiv.org/hypertex/bibstyles/
    """

    __slots__ = ("__eprint", "__archive_prefix", "__primary_class")

    def __init__(
        self, eprint: str, archive_prefix: Optional[str], primary_class: Optional[str]
    ):
        self.__eprint = validate_eprint(eprint)
        self.__archive_prefix = validate_archive_prefix(eprint, archive_prefix)
        self.__primary_class = validate_primary_class(eprint, primary_class)

    def __str__(self):
        return self.__eprint

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [
            ("eprint", self.__eprint),
            ("archive_prefix", self.__archive_prefix),
            ("primary_class", self.__primary_class),
        ]
        dict_ = {}
        for key, value in fields:
            if value:
                dict_[key] = value
        return dict_

    @property
    def eprint(self) -> str:
        """eprint field
        eg. 'hep-ph/9609357' (old style)
        or '0707.3168' (new style)
        """
        return self.__eprint

    @eprint.setter
    def eprint(self, value: str):
        self.__eprint = validate_eprint(value)

    @property
    def archive_prefix(self) -> Optional[str]:
        """necessary for new style arXiv identifiers
        eg. 'arXiv'
        """
        return self.__archive_prefix

    @archive_prefix.setter
    def archive_prefix(self, value: Optional[str]):
        self.__archive_prefix = validate_archive_prefix(self.__eprint, value)

    @property
    def primary_class(self) -> Optional[str]:
        """necessary for new style arXiv identifiers
        eg. 'physics.flu-dyn'
        """
        return self.__primary_class

    @primary_class.setter
    def primary_class(self, value: Optional[str]):
        self.__primary_class = validate_primary_class(self.__eprint, value)
