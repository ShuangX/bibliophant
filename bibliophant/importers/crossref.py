"""get bibliographic data for a DOI from crossref.org

Refer to http://labs.crossref.org/site/quick_and_dirty_api_guide.html
for more information.

This code is adapted from fxcoudert/tools/doi2bib (on GitHub).
"""

__all__ = ["doi_to_record"]


from xml.dom.minidom import parseString as parse_xml
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from typing import Dict

from ..misc import format_string, key_generator


def _get_item(container, name):
    elements = container.getElementsByTagName(name)
    if elements:
        return elements[0]
    return None


def _get_data(node):
    if node:
        return node.firstChild.data
    return None


def doi_to_record(doi: str) -> Dict:
    """Returns a record (dict / JSON) given a DOI.
    The DOI must be in the format specified by the schema,
    i.e. a string without the URL part.
    """
    params = urlencode(
        {
            "id": "doi:" + doi,
            "noredirect": "true",
            "pid": "fx.coudert@chimie-paristech.fr",
            "format": "unixref",
        }
    )
    url = Request("http://www.crossref.org/openurl/?" + params)
    doc = parse_xml(urlopen(url).read())
    records = doc.getElementsByTagName("journal")

    if not records:
        raise Exception("CrossRef returned no records")

    if len(records) != 1:
        raise Exception("CrossRef returned more than one record")

    record = records[0]

    journal_metadata = _get_item(record, "journal_metadata")
    journal_issue = _get_item(record, "journal_issue")
    journal_article = _get_item(record, "journal_article")

    authors = []
    for node in journal_article.getElementsByTagName("person_name"):
        author = {}
        last = _get_data(_get_item(node, "surname"))
        author["last"] = format_string(last)
        first = _get_data(_get_item(node, "given_name"))
        author["first"] = format_string(first)
        authors.append(author)

    journal_issue_year = _get_data(_get_item(journal_issue, "year"))
    journal_article_year = _get_data(_get_item(journal_article, "year"))
    if journal_article_year and not journal_issue_year:
        year = int(journal_article_year)
    elif journal_article_year and journal_issue_year:
        if journal_article_year == journal_issue_year:
            year = int(journal_article_year)
        else:
            raise Exception(
                f"journal_article_year = {journal_article_year} != journal_issue_year = {journal_issue_year}"
            )
    elif not journal_article_year and journal_issue_year:
        year = int(journal_issue_year)
    elif not journal_article_year and not journal_issue_year:
        raise Exception("the record does not contain a year")

    res = {}
    res["type"] = "article"
    res["key"] = key_generator(year, authors)

    title = _get_data(_get_item(journal_article, "title"))
    if title:
        res["title"] = format_string(title)

    res["authors"] = authors
    res["year"] = year

    assert doi == _get_data(_get_item(journal_article, "doi"))
    res["doi"] = doi

    if journal_metadata:
        journal = _get_data(_get_item(journal_metadata, "full_title"))
        res["journal"] = {"name": format_string(journal)}
        # journal_abbrev_title = _get_data(_get_item(journal_metadata, 'abbrev_title'))

    number = _get_data(_get_item(journal_issue, "issue"))
    if number:
        res["number"] = format_string(number)
    volume = _get_data(_get_item(journal_issue, "volume"))
    if volume:
        res["volume"] = format_string(volume)

    first_page = _get_data(_get_item(journal_article, "first_page"))
    last_page = _get_data(_get_item(journal_article, "last_page"))
    if first_page and last_page:
        res["pages"] = format_string(first_page + "--" + last_page)
    elif first_page and not last_page:
        res["pages"] = format_string(first_page)

    return res
