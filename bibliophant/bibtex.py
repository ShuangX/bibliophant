"""export bibliographic records in BibTeX format"""

_month_codes = {
    1: 'jan',
    2: 'feb',
    3: 'mar',
    4: 'apr',
    5: 'may',
    6: 'jun',
    7: 'jul',
    8: 'aug',
    9: 'sep',
    10: 'oct',
    11: 'nov',
    12: 'dec'
}


def _make_author_string(record):
    authors = []
    for author in record['authors']:
        if 'first' in author:
            authors.append(author['first'] + ' ' + author['last'])
        else:
            authors.append(author['last'])
    return " and ".join(authors)


def export(record):
    """returns a BibTeX record as a string
    The function assumes that the input is valid.
    """
    r = "@" + record['type'] + "{" + record['key'] + "},\n"
    r += "  title     = {" + record['title'] + "},\n"
    r += "  author    = {" + _make_author_string(record) + "},\n"
    r += "  year      = {" + str(record['year']) +"},\n"
    if 'month' in record:
        r += "  month     = {" + _month_codes[record['month']] + "},\n"
    if 'doi' in record:
        r += "  doi       = {" + record['doi'] + "},\n"
    if record['type'] == 'article':
        r += "  journal   = {" + record['journal'] + "},\n"
        if 'volume' in record:
            r += "  volume    = {" + record['volume'] + "},\n"
        if 'number' in record:
            r += "  number    = {" + record['number'] + "},\n"
        if 'pages' in record:
            r += "  pages     = {" + record['pages'] + "},\n"
    if record['type'] == 'book':
        r += "  publisher = {" + record['publisher']['name'] + "},\n"
        if 'address' in record['publisher']:
            r += "  address   = {" + record['publisher']['address'] + "},\n"
        if 'volume' in record:
            r += "  volume    = {" + record['volume'] + "},\n"
        if 'edition' in record:
            r += "  edition   = {" + record['volume'] + "},\n"
        if 'series' in record:
            r += "  series    = {" + record['series'] + "},\n"
    r += "}"
    return r
