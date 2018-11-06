"""This module defines a abstact base class Record.
The class contains all properties that are common to concrete types of
bibliographic records such as eg. Article and Book.
It further defines functions to validate the type and format
of the class's data members.
"""

__all__ = []

from abc import ABCMeta, abstractmethod
import re
from typing import List, Optional

from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import ModelBase
from .author import Author, author_association_table
from .url import Url
from .tag import Tag, tag_association_table


REGEX_PATTERNS = {
    "key": re.compile(r"""^[0-9]{4}[a-zA-Z]{2,}$"""),
    # cf. https://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
    "doi": re.compile(r"""(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)"""),
}


def validate_key(key: str) -> str:
    """validate the (BibTeX) key"""
    if not (isinstance(key, str) and REGEX_PATTERNS["key"].search(key)):
        raise ValueError("key must match " + REGEX_PATTERNS["key"].pattern)
    return key


def validate_title(title: str) -> str:
    """validate the field for the title"""
    if not (isinstance(title, str) and len(title) >= 6):
        raise ValueError("title must be a str with at least 6 characters")
    return title


def validate_year(year: int) -> int:
    """validate the field for the year of publication"""
    if not (isinstance(year, int) and 1800 <= year <= 2030):
        raise ValueError("year must be a int between 1800 and 2030")
    return year


def validate_authors(authors: List[Author]) -> List[Author]:
    """validate the list of authors"""
    if not isinstance(authors, list) or not authors:
        raise ValueError("authors must be a non-empty list")
    if not all(isinstance(e, Author) for e in authors):
        raise ValueError("all elements must be of type Author")
    if len(authors) > len(set(str(authors))):
        raise ValueError("elements must be unique")
    return authors


def validate_doi(doi: Optional[str]) -> Optional[str]:
    """validate the digital object identifier (DOI)"""
    if doi is not None and not (
        isinstance(doi, str) and REGEX_PATTERNS["doi"].search(doi)
    ):
        raise ValueError(
            "doi must be None or a str that matches " + REGEX_PATTERNS["doi"].pattern
        )
    return doi


def validate_month(month: Optional[int]) -> Optional[int]:
    """validate the field for the month of publication"""
    if month is not None and not (isinstance(month, int) and 1 <= month <= 12):
        raise ValueError("month must be None or a int between 1 and 12")
    return month


def validate_note(note: Optional[str]) -> Optional[str]:
    """validate the field for extra information"""
    if note is not None and not (isinstance(note, str) and len(note) >= 2):
        raise ValueError("note must be None or a str with at least 2 characters")
    return note


def validate_urls(urls: List[Url]) -> List[Url]:
    """validate the list of URLs"""
    if not isinstance(urls, list):
        raise ValueError("urls must be a list")
    if not all(isinstance(e, Url) for e in urls):
        raise ValueError("all elements must be of type Url")
    if len(urls) > len(set(urls)):
        raise ValueError("elements must be unique")
    return urls


def validate_tags(tags: List[Tag]) -> List[Tag]:
    """validate the list of tags"""
    if not isinstance(tags, list):
        raise ValueError("tags must be a list")
    if not all(isinstance(e, Tag) for e in tags):
        raise ValueError("all elements must be of type Tag")
    if len(tags) > len(set(str(tags))):
        raise ValueError("elements must be unique")
    return tags


def validate_open_access(open_access: Optional[bool]) -> Optional[bool]:
    """validate the open_access flag"""
    if open_access is not None and not isinstance(open_access, bool):
        raise ValueError("open_access must be either None or a bool")
    return open_access


class Record(ModelBase):
    """abstract base class for a bibliographic record"""

    __tablename__ = "record"

    id = Column(Integer, primary_key=True)

    record_type = Column(String(16), nullable=False)
    __mapper_args__ = {"polymorphic_on": record_type}

    __key = Column(String, nullable=False)
    __title = Column(String, nullable=False)
    __year = Column(Integer, nullable=False)
    __authors = relationship(
        "Author", secondary=author_association_table, back_populates="records"
    )
    __doi = Column(String)
    __month = Column(Integer)
    __note = Column(String)
    __urls = relationship("Url", back_populates="record")
    __tags = relationship(
        "Tag", secondary=tag_association_table, back_populates="records"
    )
    __open_access = Column(Boolean)

    # pylint: disable=dangerous-default-value, too-many-arguments
    @abstractmethod
    def __init__(
        self,
        key: str,
        title: str,
        year: int,
        authors: List[Author],
        doi: Optional[str] = None,
        month: Optional[int] = None,
        note: Optional[str] = None,
        urls: List[Url] = [],
        tags: List[Tag] = [],
        open_access: Optional[bool] = None,
    ):
        self.__key = validate_key(key)
        self.__title = validate_title(title)
        self.__year = validate_year(year)
        self.__authors = validate_authors(authors)
        self.__doi = validate_doi(doi)
        self.__month = validate_month(month)
        self.__note = validate_note(note)
        self.__urls = validate_urls(urls)
        self.__tags = validate_tags(tags)
        self.__open_access = validate_open_access(open_access)

    def __str__(self):
        return self.__key

    @abstractmethod
    def to_dict(self):
        """export all properties which are not None as a dict
        (for JSON serialization)
        """
        pass

    @hybrid_property
    def key(self) -> str:
        """unique identifier (and BibTeX key)"""
        return self.__key

    @key.setter
    def key(self, value: str):
        self.__key = validate_key(value)

    @hybrid_property
    def title(self) -> str:
        """the title of the work"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = validate_title(value)

    @hybrid_property
    def year(self) -> int:
        """the year of publication (or, if unpublished, the year of creation)"""
        return self.__year

    @year.setter
    def year(self, value: int):
        self.__year = validate_year(value)

    @hybrid_property
    def authors(self) -> List[Author]:
        """the author(s) of the work"""
        return self.__authors

    @authors.setter
    def authors(self, value: List[Author]):
        self.__authors = validate_authors(value)

    @hybrid_property
    def doi(self) -> Optional[str]:
        """digital object identifier"""
        return self.__doi

    @doi.setter
    def doi(self, value: Optional[str]):
        self.__doi = validate_doi(value)

    @hybrid_property
    def month(self) -> Optional[int]:
        """the month of publication (or, if unpublished, the year of creation)"""
        return self.__month

    @month.setter
    def month(self, value: Optional[int]):
        self.__month = validate_month(value)

    @hybrid_property
    def note(self) -> Optional[str]:
        """miscellaneous extra information"""
        return self.__note

    @note.setter
    def note(self, value: Optional[str]):
        self.__note = validate_note(value)

    @hybrid_property
    def urls(self) -> List[Url]:
        """URL(s) related to the work"""
        return self.__urls

    @urls.setter
    def urls(self, value: List[Url]):
        self.__urls = validate_urls(value)

    @hybrid_property
    def tags(self) -> List[Tag]:
        """tags / keywords related to the work"""
        return self.__tags

    @tags.setter
    def tags(self, value: List[Tag]):
        self.__tags = validate_tags(value)

    @hybrid_property
    def open_access(self) -> Optional[bool]:
        """marks if the work can be accessed freely"""
        return self.__open_access

    @open_access.setter
    def open_access(self, value: Optional[bool]):
        self.__open_access = validate_open_access(value)
