"""get bibliographic data from arxiv.org (and crossref.org)"""

from urllib.request import urlopen, Request, urlretrieve
from xml.dom.minidom import parseString as parse_xml
import os

from bibliophant.importers.crossref import _get_item, _get_data, _format_string, doi_to_record
from bibliophant.commands.add import key_generator

ROOT = '../records'


def _author_from_name(name):
    """just guessing that the last word is the last name"""
    words = name.split(' ')
    author = {
        'last': _format_string(words[-1]),
        'first': _format_string(' '.join(words[:-1]))
    }
    return author


def arxiv_id_to_record(arxiv_id):
    """returns a record (dict / JSON) given a arXiv ID"""
    url = Request('http://export.arxiv.org/api/query?id_list=' + arxiv_id)
    doc = parse_xml(urlopen(url).read())

    records = doc.getElementsByTagName('entry')

    if not records:
        raise Exception('arXiv returned no records')

    if len(records) != 1:
        raise Exception('arXiv returned more than one record')

    record = records[0]

    doi = _get_data(_get_item(record, 'arxiv:doi'))
    if doi:
        res = doi_to_record(doi)
    else:
        res = {}
        res['type'] = 'article'

        authors = []
        for author in record.getElementsByTagName('author'):
            name = _get_data(_get_item(author, 'name'))
            authors.append(_author_from_name(name))

        date = _get_data(_get_item(record, 'published'))
        if date:
            year = int(date[:4])
            month = int(date[5:7])

        if year and authors:
            res['key'] = key_generator(year, authors)

        title = _get_data(_get_item(record, 'title'))
        if title:
            res['title'] = _format_string(title)

        if authors:
            res['authors'] = authors

        if date:
            res['year'] = year
            res['month'] = month

        res['journal'] = 'arXiv e-print'

    res['eprint'] = {}
    if '/' not in arxiv_id:
        # new style id
        categorys = record.getElementsByTagName('category')
        primary_category = categorys[0].getAttribute('term')
        res['eprint']['archive_prefix'] = 'arXiv'
        res['eprint']['eprint'] = arxiv_id
        res['eprint']['primary_class'] = primary_category
    else:
        # old style (before April 2007) id
        res['eprint']['eprint'] = arxiv_id

    # for link in record.getElementsByTagName('link'):
    #     if link.getAttribute('title') == 'pdf':
    #             pdf_link = link.getAttribute('href')
    #             break
    # if pdf_link:
    #     if 'urls' not in res:
    #         res['urls'] = []
    #     res['urls'].append(
    #         {
    #             'url': pdf_link,
    #             'description': 'PDF on arXiv'
    #         }
    #     )

    summary = _get_data(_get_item(record, 'summary'))
    if summary:
        res['abstract'] = _format_string(summary)

    return res


def download_arxiv_eprint(record, overwrite=False):
    """downloads the latest PDF for a given arXiv id"""
    try:
        arxiv_id = record['eprint']['eprint']
    except:
        raise Exception('the record has no eprint field that holds a arXiv id')

    record_folder = os.path.join(ROOT, record['key'])

    file_name = record['title'].replace(':', '')
    pdf_file_path = os.path.join(record_folder, file_name + '.pdf')

    if not overwrite and os.path.exists(pdf_file_path):
        raise Exception('the PDF file already exists')

    _, msg = urlretrieve('https://arxiv.org/pdf/' + arxiv_id + '.pdf', pdf_file_path)

    if msg.get_content_type() != 'application/pdf':
        os.remove(pdf_file_path)
        raise Exception('something went wrong with the download')
