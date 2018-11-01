"""export bibliographic records in BibTeX format

It is assumed that UTF8 is understood by the software that consumes the output.
If you need any char replacement for non-UTF8 software you may adapt this from
fxcoudert/tools/doi2bib (on GitHub).
"""
__all__ = ['record_to_bibtex', 'records_to_bibfile']

import pathlib

_MONTH_CODES = {
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


def record_to_bibtex(record):
    """Returns a BibTeX record as a string.
    The function assumes that the input is valid.
    """
    bibtex = "@" + record['type'] + "{" + record['key'] + ",\n"
    bibtex += "\ttitle         = {" + record['title'] + "},\n"
    bibtex += "\tauthor        = {" + _make_author_string(record) + "},\n"
    bibtex += "\tyear          = {" + str(record['year']) +"},\n"
    if 'month' in record:
        bibtex += "\tmonth         = {" + _MONTH_CODES[record['month']] + "},\n"
    if 'doi' in record:
        bibtex += "\tdoi           = {" + record['doi'] + "},\n"
    if record['type'] == 'article':
        bibtex += "\tjournal       = {" + record['journal'] + "},\n"
        if 'volume' in record:
            bibtex += "\tvolume        = {" + record['volume'] + "},\n"
        if 'number' in record:
            bibtex += "\tnumber        = {" + record['number'] + "},\n"
        if 'pages' in record:
            bibtex += "\tpages         = {" + record['pages'] + "},\n"
        if 'eprint' in record:
            if '/' not in record['eprint']['eprint']:
                # new style id
                bibtex += "\tarchivePrefix = {" + record['eprint']['archive_prefix'] + "},\n"
                bibtex += "\teprint        = {" + record['eprint']['eprint'] + "},\n"
                bibtex += "\tprimaryClass  = {" + record['eprint']['primary_class'] + "},\n"
            else:
                # old style (before April 2007) id
                bibtex += "\teprint        = {" + record['eprint']['eprint'] + "},\n"
    if record['type'] == 'book':
        bibtex += "\tpublisher     = {" + record['publisher']['name'] + "},\n"
        if 'address' in record['publisher']:
            bibtex += "\taddress       = {" + record['publisher']['address'] + "},\n"
        if 'volume' in record:
            bibtex += "\tvolume        = {" + record['volume'] + "},\n"
        if 'edition' in record:
            bibtex += "\tedition       = {" + record['volume'] + "},\n"
        if 'series' in record:
            bibtex += "\tseries        = {" + record['series'] + "},\n"
    bibtex += "}"
    return bibtex


def records_to_bibfile(records, full_path, overwrite=False):
    """Takes an iterable of records` and writes the BibTeX for all of them
    in a file.
    full_path can be relative or absolute and must end in '.bib'.
    If the file already exists then overwrite must be True for something to happen.
    """
    full_path = pathlib.Path(full_path).absolute()
    if not full_path.parent.is_dir():
        raise Exception('the directory does not exist')
    if full_path.name[-4:] != '.bib':
        raise Exception("the file extension must be '.bib'")
    if full_path.exists() and not overwrite:
        raise Exception('the file already exists')
    with open(full_path, 'w') as file:
        for record in records:
            file.write(record_to_bibtex(record) + '\n\n')
