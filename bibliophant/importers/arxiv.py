"""get bibliographic data from arxiv.org (and crossref.org)"""

__all__ = ["arxiv_id_to_record", "download_arxiv_eprint"]


from urllib.request import urlopen, Request, urlretrieve
from xml.dom.minidom import parseString as parse_xml
from pathlib import Path
from typing import Dict, Optional

from .crossref import _get_item, _get_data, doi_to_record
from ..models.article import Article
from ..misc import format_string, key_generator


def _author_from_name(name: str) -> Dict[str, str]:
    """Turns a name into a author by guessing that
    the last word is the last name.
    """
    words = name.split(" ")
    author = {
        "last": format_string(words[-1]),
        "first": format_string(" ".join(words[:-1])),
    }
    return author


def arxiv_id_to_record(arxiv_id: str) -> Dict:
    """Returns a record (dict / JSON) for a given arXiv ID."""
    url = Request("http://export.arxiv.org/api/query?id_list=" + arxiv_id)
    xml_data = urlopen(url).read()
    doc = parse_xml(xml_data)

    records = doc.getElementsByTagName("entry")

    if not records:
        raise Exception("arXiv returned no records")

    if len(records) != 1:
        raise Exception("arXiv returned more than one record")

    record = records[0]

    doi = _get_data(_get_item(record, "arxiv:doi"))
    if doi:
        res = doi_to_record(doi)
    else:
        res = {}
        res["type"] = "article"

        authors = []
        for author in record.getElementsByTagName("author"):
            name = _get_data(_get_item(author, "name"))
            authors.append(_author_from_name(name))

        date = _get_data(_get_item(record, "published"))
        if date:
            year = int(date[:4])
            month = int(date[5:7])

        if year and authors:
            res["key"] = key_generator(year, authors)

        title = _get_data(_get_item(record, "title"))
        if title:
            res["title"] = format_string(title)

        if authors:
            res["authors"] = authors

        if date:
            res["year"] = year
            res["month"] = month

        res["journal"] = {"name": "arXiv e-print"}

    res["eprint"] = {}
    if "/" not in arxiv_id:
        # new style id
        categorys = record.getElementsByTagName("category")
        primary_category = categorys[0].getAttribute("term")
        res["eprint"]["archive_prefix"] = "arXiv"
        res["eprint"]["eprint"] = arxiv_id
        res["eprint"]["primary_class"] = primary_category
    else:
        # old style (before April 2007) id
        res["eprint"]["eprint"] = arxiv_id

    res["open_access"] = True

    summary = _get_data(_get_item(record, "summary"))
    if summary:
        res["abstract"] = format_string(summary)

    return res


def download_arxiv_eprint(
    article: Article, root_folder: Path, overwrite: Optional[bool] = False
):
    """Downloads the latest PDF for a given article with arXiv ID.
    Raises ValueError if the article has no eprint field.
    Raises FileNotFoundError if the record folder is not found.
    Raises FileExistsError if the PDF file already exists and overwrite is False.
    Raises RuntimeError if the file can't be downloaded.
    """
    try:
        arxiv_id = article.eprint.eprint
    except:
        raise ValueError("the article has no eprint field that holds a arXiv id")

    record_folder = root_folder / article.key
    if not record_folder.is_dir():
        raise FileNotFoundError(f"the record folder {record_folder} does not exist")

    pdf_file = record_folder / (article.title.replace(":", "") + ".pdf")

    if pdf_file.exists() and not overwrite:
        raise FileExistsError("the PDF file already exists")

    _, msg = urlretrieve("https://arxiv.org/pdf/" + arxiv_id + ".pdf", pdf_file)

    if msg.get_content_type() != "application/pdf":
        pdf_file.unlink()
        raise RuntimeError("something went wrong with the download")
