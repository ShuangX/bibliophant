"""get bibliographic data for a DOI from crossref.org

Refer to http://labs.crossref.org/site/quick_and_dirty_api_guide.html
for more information.

This code is adapted from fxcoudert/tools on GitHub.
"""

from xml.dom.minidom import parseString as parse_xml
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from commands.add import key_generator
from unicodedata import normalize


def _get_item(container, name):
    list = container.getElementsByTagName(name)
    if len(list) == 0:
        return None
    else:
        return list[0]


def _get_data(node):
    if node is None:
        return None
    else:
        return node.firstChild.data


def get_record(doi):
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
        author['last'] = normalize('NFKD', last)
        first = _get_data(_get_item(node, "given_name"))
        author['first'] = normalize('NFKD', first)
        authors.append(author)

    journal_issue_year = _get_data(_get_item(journal_issue, 'year'))
    journal_article_year = _get_data(_get_item(journal_article, 'year'))
    assert(journal_issue_year == journal_article_year)
    year = int(journal_issue_year)

    res = {}
    res['type'] = 'article'
    res['key'] = key_generator(authors, year)

    title = _get_data(_get_item(journal_article, 'title'))
    res['title'] = normalize('NFKD', title)

    res['authors'] = authors
    res['year'] = year

    assert doi == _get_data(_get_item(journal_article, 'doi'))
    res['doi'] = doi

    if journal_metadata:
        journal = _get_data(_get_item(journal_metadata, 'full_title'))
        res['journal'] = normalize('NFKD', journal)
        # journal_abbrev_title = _get_data(_get_item(journal_metadata, 'abbrev_title'))

    number = _get_data(_get_item(journal_issue, 'issue'))
    if number:
        res['number'] = normalize('NFKD', number)
    volume = _get_data(_get_item(journal_issue, "volume"))
    if volume:
        res['volume'] = normalize('NFKD', volume)

    first_page = _get_data(_get_item(journal_article, 'first_page'))
    last_page = _get_data(_get_item(journal_article, 'last_page'))
    res['pages'] = normalize('NFKD', first_page + '--' + last_page)

    return res
