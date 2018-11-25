"""export bibliographic records in BibTeX format

It is assumed that UTF8 is understood by the software that consumes the output.
If you need any char replacement for non-UTF8 software you may adapt this from
fxcoudert/tools/doi2bib (on GitHub).
"""

__all__ = ["record_to_bibtex", "records_to_bibfile", "collection_to_bibfile"]


from pathlib import Path
from typing import List, Iterable, Optional, Union

from ..models.record import Record, Author


_MONTH_CODES = {
    1: "jan",
    2: "feb",
    3: "mar",
    4: "apr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "aug",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dec",
}


def _make_author_string(authors: List[Author]) -> str:
    author_names = []
    for author in authors:
        if author.first:
            author_names.append(author.first + " " + author.last)
        else:
            author_names.append(author.last)
    return " and ".join(author_names)


# pylint: disable=R0912
def record_to_bibtex(record: Record) -> str:
    """Returns a BibTeX record as a string.
    The function assumes that the input is valid.
    """
    bibtex = "@" + record.record_type + "{" + record.key + ",\n"
    bibtex += "\ttitle         = {" + record.title + "},\n"
    bibtex += "\tauthor        = {" + _make_author_string(record.authors) + "},\n"
    bibtex += "\tyear          = {" + str(record.year) + "},\n"
    if record.month:
        bibtex += "\tmonth         = {" + _MONTH_CODES[record.month] + "},\n"
    if record.doi:
        bibtex += "\tdoi           = {" + record.doi + "},\n"
    if record.record_type == "article":
        bibtex += "\tjournal       = {" + record.journal.name + "},\n"
        if record.volume:
            bibtex += "\tvolume        = {" + record.volume + "},\n"
        if record.number:
            bibtex += "\tnumber        = {" + record.number + "},\n"
        if record.pages:
            bibtex += "\tpages         = {" + record.pages + "},\n"
        if record.eprint:
            if "/" not in record.eprint.eprint:
                # new style id
                bibtex += "\tarchivePrefix = {" + record.eprint.archive_prefix + "},\n"
                bibtex += "\teprint        = {" + record.eprint.eprint + "},\n"
                bibtex += "\tprimaryClass  = {" + record.eprint.primary_class + "},\n"
            else:
                # old style id (before April 2007)
                bibtex += "\teprint        = {" + record.eprint.eprint + "},\n"
    if record.record_type == "book":
        bibtex += "\tpublisher     = {" + record.publisher.name + "},\n"
        if record.publisher.address:
            bibtex += "\taddress       = {" + record.publisher.address + "},\n"
        if record.volume:
            bibtex += "\tvolume        = {" + record.volume + "},\n"
        if record.edition:
            bibtex += "\tedition       = {" + record.edition + "},\n"
        if record.series:
            bibtex += "\tseries        = {" + record.series + "},\n"
    bibtex += "}"
    return bibtex


def records_to_bibfile(
    records: Iterable[Record],
    full_path: Union[Path, str],
    overwrite: Optional[bool] = False,
):
    """Takes an iterable of records` and writes the BibTeX for all of them
    in a file.
    full_path can be relative or absolute and must end in '.bib'.
    Raises FileNotFoundError if the specified directory does not exist.
    Raises ValueError if the file extension is not 'bib'.
    Raises FileExistsError if the file already exists and overwrite is False.
    """
    full_path = Path(full_path)
    if not full_path.parent.is_dir():
        raise FileNotFoundError(f"the directory {full_path.parent} does not exist")
    if full_path.suffix != ".bib":
        raise ValueError("the file extension must be '.bib'")
    if full_path.exists() and not overwrite:
        raise FileExistsError(f"the file {full_path} already exists")
    with open(full_path, "w") as file:
        for record in records:
            file.write(record_to_bibtex(record) + "\n\n")


def collection_to_bibfile(
    session: "sqlalchemy.orm.session.Session",
    full_path: Union[Path, str],
    overwrite: Optional[bool] = False,
):
    """Exports the entire collection to a bibfile.
    Refer to records_to_bibfile for further details.
    """
    records_to_bibfile(
        records=session.query(Record).order_by(Record.key.asc()),
        full_path=full_path,
        overwrite=overwrite,
    )
