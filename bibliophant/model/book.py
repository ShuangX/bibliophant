"""This module defines a class Book
which inherits from the abstact base class Record.

It also defines a class Eprint which stores a reference
to an eprint on a site such as the arXiv.

It further defines functions to validate the type and format
of the class's data members.
"""

__all__ = []

from typing import List, Optional

from .record import Record
from .author import Author
from .publisher import Publisher
from .url import Url
from .tag import Tag


def validate_publisher(publisher: Publisher) -> Publisher:
    """validate the reference to the publisher"""
    if not isinstance(publisher, Publisher):
        raise ValueError("publisher must be of type Publisher")
    return publisher


def validate_volume(volume: Optional[str]) -> Optional[str]:
    """validate the volume field (for multi-volume books)"""
    if volume is not None and not (isinstance(volume, str) and len(volume) >= 1):
        raise ValueError("volume must be a str with at least 1 character")
    return volume


def validate_edition(edition: Optional[str]) -> Optional[str]:
    """validate the edition field"""
    if edition is not None and not (isinstance(edition, str) and len(edition) >= 1):
        raise ValueError("edition must be a str with at least 1 character")
    return edition


def validate_series(series: Optional[str]) -> Optional[str]:
    """validate the series field"""
    if series is not None and not (isinstance(series, str) and len(series) >= 3):
        raise ValueError("series must be a str with at least 3 character")
    return series


class Book(Record):
    """class for a bibliographic record of type book"""

    __slots__ = ("__publisher", "__volume", "__edition", "__series")

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
        urls: Optional[List[Url]] = [],
        tags: Optional[List[Tag]] = [],
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
        self.__publisher = validate_publisher(publisher)
        self.__volume = validate_volume(volume)
        self.__edition = validate_edition(edition)
        self.__series = validate_series(series)

    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
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
        dict_ = {}
        dict_["type"] = "book"
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
        return self.__publisher

    @publisher.setter
    def publisher(self, value: Publisher):
        self.__publisher = validate_publisher(value)

    @property
    def volume(self) -> Optional[str]:
        """the volume of a multi-volume book"""
        return self.__volume

    @volume.setter
    def volume(self, value: Optional[str]):
        self.__volume = validate_volume(value)

    @property
    def edition(self) -> Optional[str]:
        """the edition of a book ("First" or "Second")"""
        return self.__edition

    @edition.setter
    def edition(self, value: Optional[str]):
        self.__edition = validate_edition(value)

    @property
    def series(self) -> Optional[str]:
        """the name of the book series"""
        return self.__series

    @series.setter
    def series(self, value: Optional[str]):
        self.__series = validate_series(value)
