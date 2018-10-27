"""JSON schema for bibliographic records of type article
The main idea is documented in general.py
"""

import general

required_properties = general.required_properties + ['journal']
# 'volume' might also be considered as a required property!

properties = general.properties.copy()

properties['type'] = {
    'description': 'this bibliographic record is of type article',
    'const': 'article'
}

properties['journal'] = {
    'description': 'the journal or magazine the work was published in',
    'type': 'string',
    'minLength': 4
}

properties['volume'] = {
    'description': 'the volume of the journal',
    'type': 'string',
    'minLength': 1
}

properties['number'] = {
    'description': "the '(issue) number' of a journal (this is not the 'article number' assigned by some journals)",
    'type': 'string',
    'minLength': 1
}

properties['pages'] = {
    'description': 'page numbers, separated either by commas or double-hyphens',
    'type': 'string',
    'minLength': 1
}

properties['abstract'] = {
    'description': 'the abstract of the article',
    'type': 'string',
    'minLength': 10
}

schema = general.Schema(required_properties, properties)
