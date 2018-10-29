"""this module is about adding new biblopgraphic records"""


def key_generator(authors, year):
    """adds a key to the record"""
    key = str(year)
    for author in authors:
        key += author['last']
    return key.replace(' ', '')
