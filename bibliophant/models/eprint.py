"""This module defines a class Eprint which stores a reference
to an eprint on a site such as the arXiv.
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


def validate_eprint(eprint: str) -> str:
    """validate the eprint field"""
    if not isinstance(eprint, str):
        raise ValueError("eprint must be a str")

    eprint = format_string(eprint)
    if len(eprint) < 9:
        raise ValueError("eprint must have at least 9 characters")

    return eprint


def validate_archive_prefix(
    eprint: str, archive_prefix: Optional[str]
) -> Optional[str]:
    """validate the archive_prefix field
    based on the content of the eprint field
    """
    if "/" in eprint:  # old style identifiers don't require the field
        if archive_prefix is None:
            return None
        raise ValueError("archive_prefix is not required for old-style identifiers")

    else:  # new style identifiers do require it
        if not isinstance(archive_prefix, str):
            raise ValueError("archive_prefix must be a str")

        archive_prefix = format_string(archive_prefix)
        if len(archive_prefix) < 5:
            raise ValueError("archive_prefix must have at least 5 characters")

        return archive_prefix


def validate_primary_class(eprint: str, primary_class: Optional[str]) -> Optional[str]:
    """validate the primary_class field
    based on the content of the eprint field
    """
    if "/" in eprint:  # old style identifiers don't require the field
        if primary_class is None:
            return None
        raise ValueError("primary_class is not required for old-style identifiers")

    else:  # new style identifiers do require it
        if not isinstance(primary_class, str):
            raise ValueError("primary_class must be a str")

        primary_class = format_string(primary_class)
        if len(primary_class) < 5:
            raise ValueError("primary_class must have at least 5 characters")

        return primary_class


class Eprint(ModelBase):
    """class for referring to (arXiv) eprints
    For further information go to:
    https://arxiv.org/hypertex/bibstyles/
    """

    __tablename__ = "eprint"

    id = Column(Integer, primary_key=True)

    article = relationship("Article", back_populates="_eprint", uselist=False)

    _eprint = Column(String, nullable=False)
    _archive_prefix = Column(String)
    _primary_class = Column(String)

    def __init__(
        self,
        eprint: str,
        archive_prefix: Optional[str] = None,
        primary_class: Optional[str] = None,
    ):
        self._eprint = validate_eprint(eprint)
        self._archive_prefix = validate_archive_prefix(eprint, archive_prefix)
        self._primary_class = validate_primary_class(eprint, primary_class)

    def __repr__(self):
        res = 'Eprint("' + self._eprint + '"'
        if self._archive_prefix:
            res += ', archive_prefix="' + self._archive_prefix + '"'
        if self._primary_class:
            res += ', primary_class="' + self._primary_class + '"'
        res += ")"
        return res

    def __str__(self):
        return self._eprint

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        fields = [
            ("eprint", self._eprint),
            ("archive_prefix", self._archive_prefix),
            ("primary_class", self._primary_class),
        ]
        return {key: value for key, value in fields if value}

    @hybrid_property
    def eprint(self) -> str:
        """eprint field
        eg. 'hep-ph/9609357' (old style)
        or '0707.3168' (new style)
        """
        return self._eprint

    @eprint.setter
    def eprint(self, value: str):
        self._eprint = validate_eprint(value)

    @hybrid_property
    def archive_prefix(self) -> Optional[str]:
        """necessary for new style arXiv identifiers
        eg. 'arXiv'
        """
        return self._archive_prefix

    @archive_prefix.setter
    def archive_prefix(self, value: Optional[str]):
        self._archive_prefix = validate_archive_prefix(self.__eprint, value)

    @hybrid_property
    def primary_class(self) -> Optional[str]:
        """necessary for new style arXiv identifiers
        eg. 'physics.flu-dyn'
        """
        return self._primary_class

    @primary_class.setter
    def primary_class(self, value: Optional[str]):
        self._primary_class = validate_primary_class(self.__eprint, value)
