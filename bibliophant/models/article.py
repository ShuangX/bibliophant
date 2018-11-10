"""This module defines a class Article
which inherits from the abstact base class Record.
It further defines functions to validate the type and format
of the class's data members.
"""

# TODO: volume might also be considered as a required property!

__all__ = []

from typing import List, Optional

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .record import Record
from .author import Author
from .url import Url
from .tag import Tag
from .eprint import Eprint


def validate_journal(journal: str) -> str:
    """validate the field for the journal's name"""
    if not (isinstance(journal, str) and len(journal) >= 4):
        raise ValueError("journal must be a str with at least 4 characters")
    return journal


def validate_volume(volume: Optional[str]) -> Optional[str]:
    """validate the field for the journal's volume"""
    if volume is not None and not (isinstance(volume, str) and len(volume) >= 1):
        raise ValueError("volume must be a str with at least 1 character")
    return volume


def validate_number(number: Optional[str]) -> Optional[str]:
    """validate the field for the journal's (issue) number"""
    if number is not None and not (isinstance(number, str) and len(number) >= 1):
        raise ValueError("number must be a str with at least 1 character")
    return number


def validate_pages(pages: Optional[str]) -> Optional[str]:
    """validate the page number field of the article"""
    if pages is not None and not (isinstance(pages, str) and len(pages) >= 1):
        raise ValueError("pages must be a str with at least 1 character")
    return pages


def validate_eprint(eprint: Optional[Eprint]) -> Optional[Eprint]:
    """validate the reference to a corresponding eprint"""
    if eprint is not None and not isinstance(eprint, Eprint):
        raise ValueError("eprint must be of type Eprint")
    return eprint


def validate_abstract(abstract: Optional[str]) -> Optional[str]:
    """validate the field for the article's abstract"""
    if abstract is not None and not (isinstance(abstract, str) and len(abstract) >= 10):
        raise ValueError("abstract must be a str with at least 10 characters")
    return abstract


class Article(Record):
    """class for a bibliographic record of type article"""

    __tablename__ = "article"
    id = Column(None, ForeignKey("record.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "article"}

    _journal = Column(String, nullable=False)
    _volume = Column(String)
    _number = Column(String)
    _pages = Column(String)
    eprint_id = Column(Integer, ForeignKey("eprint.id"))
    _eprint = relationship("Eprint", back_populates="article")
    _abstract = Column(String)

    # pylint: disable=dangerous-default-value, too-many-arguments, too-many-locals
    def __init__(
        self,
        key: str,
        title: str,
        year: int,
        authors: List[Author],
        journal: str,
        doi: Optional[str] = None,
        month: Optional[int] = None,
        note: Optional[str] = None,
        urls: List[Url] = [],
        tags: List[Tag] = [],
        open_access: Optional[bool] = None,
        volume: Optional[str] = None,
        number: Optional[str] = None,
        pages: Optional[str] = None,
        eprint: Optional[Eprint] = None,
        abstract: Optional[str] = None,
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
        self._journal = validate_journal(journal)
        self._volume = validate_volume(volume)
        self._number = validate_number(number)
        self._pages = validate_pages(pages)
        self._eprint = validate_eprint(eprint)
        self._abstract = validate_abstract(abstract)

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
            ("journal", self.journal),
            ("volume", self.volume),
            ("number", self.number),
            ("pages", self.pages),
            ("doi", self.doi),
            ("eprint", self.eprint),
            ("open_access", self.open_access),
            ("urls", self.urls),
            ("abstract", self.abstract),
            ("note", self.note),
        ]
        dict_ = {}
        dict_["type"] = "article"
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

    @hybrid_property
    def journal(self) -> str:
        """the journal or magazine the work was published in"""
        return self._journal

    @journal.setter
    def journal(self, value: str):
        self._journal = validate_journal(value)

    @hybrid_property
    def volume(self) -> Optional[str]:
        """the volume of the journal"""
        return self._volume

    @volume.setter
    def volume(self, value: Optional[str]):
        self._volume = validate_volume(value)

    @hybrid_property
    def number(self) -> Optional[str]:
        """the '(issue) number' of a journal
        (this is not the 'article number'
        assigned by some journals)
        """
        return self._number

    @number.setter
    def number(self, value: Optional[str]):
        self._number = validate_number(value)

    @hybrid_property
    def pages(self) -> Optional[str]:
        """page numbers
        separated either by commas or double-hyphens
        """
        return self._pages

    @pages.setter
    def pages(self, value: Optional[str]):
        self._pages = validate_pages(value)

    @hybrid_property
    def eprint(self) -> Optional[Eprint]:
        """reference to an (arXiv) eprint"""
        return self._eprint

    @eprint.setter
    def eprint(self, value: Optional[Eprint]):
        if value and not isinstance(value, Eprint):
            raise ValueError("eprint must be of type Eprint")
        self._eprint = value

    @hybrid_property
    def abstract(self) -> Optional[str]:
        """the abstract of the article"""
        return self._abstract

    @abstract.setter
    def abstract(self, value: Optional[str]):
        self._abstract = validate_abstract(value)
