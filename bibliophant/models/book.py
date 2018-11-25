"""This module defines a class Book
which inherits from the abstact base class Record.

It also defines a class Eprint which stores a reference
to an eprint on a site such as the arXiv.

It further defines functions to validate the type and format
of the class's data members.
"""

__all__ = []


from typing import List, Optional

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .record import Record
from .author import Author
from .publisher import Publisher
from .url import Url
from .tag import Tag

from ..misc import format_string


def validate_publisher(publisher: Publisher) -> Publisher:
    """validate the reference to the publisher"""
    if not isinstance(publisher, Publisher):
        raise ValueError("publisher must be of type Publisher")
    return publisher


def validate_volume(volume: Optional[str]) -> Optional[str]:
    """validate the volume field (for multi-volume books)"""
    if volume is None:
        return None

    if not isinstance(volume, str):
        raise ValueError("volume must be a str")

    volume = format_string(volume)
    if len(volume) == 0:
        raise ValueError("volume must have at least 1 character")

    return volume


def validate_edition(edition: Optional[str]) -> Optional[str]:
    """validate the edition field"""
    if edition is None:
        return None

    if not isinstance(edition, str):
        raise ValueError("edition must be a str")

    edition = format_string(edition)
    if len(edition) == 0:
        raise ValueError("edition must have at least 1 character")

    return edition


def validate_series(series: Optional[str]) -> Optional[str]:
    """validate the series field"""
    if series is None:
        return None

    if not isinstance(series, str):
        raise ValueError("series must be a str")

    series = format_string(series)
    if len(series) < 3:
        raise ValueError("series must have at least 3 character")

    return series


class Book(Record):
    """class for a bibliographic record of type book"""

    __tablename__ = "book"
    id = Column(None, ForeignKey("record.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "book"}

    publisher_id = Column(Integer, ForeignKey("publisher.id"))
    _publisher = relationship("Publisher", back_populates="books")
    _volume = Column(String)
    _edition = Column(String)
    _series = Column(String)

    # pylint: disable=dangerous-default-value, too-many-arguments, too-many-locals
    def __init__(
        self,
        key: str,
        title: str,
        year: int,
        authors: List[Author],
        publisher: Publisher,
        doi: Optional[str] = None,
        month: Optional[int] = None,
        note: Optional[str] = None,
        urls: List[Url] = [],
        tags: List[Tag] = [],
        open_access: Optional[bool] = None,
        volume: Optional[str] = None,
        edition: Optional[str] = None,
        series: Optional[str] = None,
    ):
        super().__init__(
            key=key,
            title=title,
            year=year,
            authors=authors,
            doi=doi,
            month=month,
            note=note,
            urls=urls,
            tags=tags,
            open_access=open_access,
        )
        self._publisher = validate_publisher(publisher)
        self._volume = validate_volume(volume)
        self._edition = validate_edition(edition)
        self._series = validate_series(series)

    def __repr__(self):
        res = 'Book("' + self.key + '"'
        res += ', "' + self.title + '"'
        res += ", " + str(self.year)
        res += ", " + repr(self.authors)
        res += ", " + repr(self.publisher)
        if self.doi:
            res += ', doi="' + self.doi + '"'
        if self.month:
            res += ", month=" + str(self.month)
        if self.note:
            res += ', note="' + self.doi + '"'
        if self.urls:
            res += ", urls=" + repr(self.urls)
        if self.tags:
            res += ", tags=" + repr(self.tags)
        if self.open_access:
            res += ", open_access=" + str(self.open_access)
        if self.volume:
            res += ', volume="' + self.volume + '"'
        if self.edition:
            res += ', edition="' + self.edition + '"'
        if self.series:
            res += ', series="' + self.series + '"'
        res += ")"
        return res

    def to_dict(self):
        """Export all properties of the model which are not None as a dict.
        This is used for JSON serialization.
        """
        fields = [
            ("key", self.key),
            ("title", self.title),
            ("year", self.year),
            ("month", self.month),
            ("authors", self.authors),
            ("tags", self.tags),
            ("publisher", self.publisher),
            ("volume", self.volume),
            ("edition", self.edition),
            ("series", self.series),
            ("doi", self.doi),
            ("open_access", self.open_access),
            ("urls", self.urls),
            ("note", self.note),
        ]
        dict_ = {"type": "book"}
        for key, value in fields:
            if value:
                if isinstance(value, list):
                    dict_[key] = [
                        e.to_dict() if hasattr(e, "to_dict") else e for e in value
                    ]
                elif hasattr(value, "to_dict"):
                    dict_[key] = value.to_dict()
                else:
                    dict_[key] = value
        return dict_

    @property
    def publisher(self) -> Publisher:
        """the journal or magazine the work was published in"""
        return self._publisher

    @publisher.setter
    def publisher(self, value: Publisher):
        self._publisher = validate_publisher(value)

    @property
    def volume(self) -> Optional[str]:
        """the volume of a multi-volume book"""
        return self._volume

    @volume.setter
    def volume(self, value: Optional[str]):
        self._volume = validate_volume(value)

    @property
    def edition(self) -> Optional[str]:
        """the edition of a book ("First" or "Second")"""
        return self._edition

    @edition.setter
    def edition(self, value: Optional[str]):
        self._edition = validate_edition(value)

    @property
    def series(self) -> Optional[str]:
        """the name of the book series"""
        return self._series

    @series.setter
    def series(self, value: Optional[str]):
        self._series = validate_series(value)
