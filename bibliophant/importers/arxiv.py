"""get bibliographic data from arxiv.org (and crossref.org)"""

from urllib.request import urlopen, Request
from xml.dom.minidom import parseString as parse_xml
from unicodedata import normalize

from bibliophant.importers.crossref import _get_item, _get_data, doi_to_record


def arxiv_id_to_record(arxiv_id):
    """returns a record (dict / JSON) given a arXiv ID"""
    url = Request('http://export.arxiv.org/api/query?id_list=' + arxiv_id)
    doc = parse_xml(urlopen(url).read())

    records = doc.getElementsByTagName('entry')

    if len(records) == 0:
        raise Exception('arXiv returned no records')

    if (len(records) != 1):
        raise Exception('arXiv returned more than one record')

    record = records[0]

    doi = _get_data(_get_item(record, 'arxiv:doi'))
    if not doi:
        raise Exception('arXiv entry does not have a DOI')

    res = doi_to_record(doi)

    for link in record.getElementsByTagName('link'):
        if link.hasAttribute('title'):
            if link.getAttribute('title') == 'pdf':
                pdf_link = link.getAttribute('href')
                break
    if pdf_link:
        if 'urls' not in res:
            res['urls'] = []
        res['urls'].append(
            {
                'url': pdf_link,
                'description': 'PDF on arXiv'
            }
        )

    summary = _get_data(_get_item(record, 'summary'))
    if summary:
        res['abstract'] = normalize('NFKD', summary).strip().replace('\n', ' ')

    return res
