"""get bibliographic data for a DOI from crossref.org

Refer to http://labs.crossref.org/site/quick_and_dirty_api_guide.html
for more information.

This code is adapted from fxcoudert/tools/doi2bib (on GitHub).
"""

from xml.dom.minidom import parseString as parse_xml
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from unicodedata import normalize

from bibliophant.commands.add import key_generator


def _get_item(container, name):
    elements = container.getElementsByTagName(name)
    if len(elements) == 0:
        return None
    else:
        return elements[0]


def _get_data(node):
    if node is None:
        return None
    else:
        return node.firstChild.data


_replacements = {
    '\ufb01': 'fi',
    '\n': ' '
}


def _format_string(string):
    string = normalize('NFKD', string).strip()
    l = (_replacements[c] if c in _replacements else c for c in string)
    return ''.join(l)


def doi_to_record(doi):
    """returns a record (dict / JSON) given a DOI
    The DOI must be in the format specified by the schema,
    i.e. a string without the URL part.
    """
    params = urlencode(
        {
            'id': 'doi:' + doi,
            'noredirect': 'true',
            'pid': 'fx.coudert@chimie-paristech.fr',
            'format': 'unixref'
        }
    )
    url = Request('http://www.crossref.org/openurl/?' + params)
    doc = parse_xml(urlopen(url).read())
    records = doc.getElementsByTagName('journal')

    if len(records) == 0:
        raise Exception('CrossRef returned no records')

    if (len(records) != 1):
        raise Exception('CrossRef returned more than one record')

    record = records[0]

    journal_metadata = _get_item(record, 'journal_metadata')
    journal_issue = _get_item(record, 'journal_issue')
    journal_article = _get_item(record, 'journal_article')

    authors = []
    for node in journal_article.getElementsByTagName('person_name'):
        author = {}
        last = _get_data(_get_item(node, "surname"))
        author['last'] = _format_string(last)
        first = _get_data(_get_item(node, "given_name"))
        author['first'] = _format_string(first)
        authors.append(author)

    journal_issue_year = _get_data(_get_item(journal_issue, 'year'))
    journal_article_year = _get_data(_get_item(journal_article, 'year'))
    if journal_article_year and not journal_issue_year:
        year = int(journal_article_year)
    elif journal_article_year and journal_issue_year:
        if journal_article_year == journal_issue_year:
            year = int(journal_article_year)
        else:
            raise Exception(f'journal_article_year = {journal_article_year} != journal_issue_year = {journal_issue_year}')
    elif not journal_article_year and journal_issue_year:
        year = int(journal_issue_year)
    elif not journal_article_year and not journal_issue_year:
        raise Exception('the record does not contain a year')

    res = {}
    res['type'] = 'article'
    res['key'] = key_generator(authors, year)

    title = _get_data(_get_item(journal_article, 'title'))
    if title:
        res['title'] = _format_string(title)

    res['authors'] = authors
    res['year'] = year

    assert doi == _get_data(_get_item(journal_article, 'doi'))
    res['doi'] = doi

    if journal_metadata:
        journal = _get_data(_get_item(journal_metadata, 'full_title'))
        res['journal'] = _format_string(journal)
        # journal_abbrev_title = _get_data(_get_item(journal_metadata, 'abbrev_title'))

    number = _get_data(_get_item(journal_issue, 'issue'))
    if number:
        res['number'] = _format_string(number)
    volume = _get_data(_get_item(journal_issue, "volume"))
    if volume:
        res['volume'] = _format_string(volume)

    first_page = _get_data(_get_item(journal_article, 'first_page'))
    last_page = _get_data(_get_item(journal_article, 'last_page'))
    res['pages'] = _format_string(first_page + '--' + last_page)

    return res
