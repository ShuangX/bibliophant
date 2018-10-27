"""JSON schema for bibliographic records

There are various types of records (eg. article, book, ...).
In this file properties that are common to all record types are defined.

The JSON schema follows the standard described at http://json-schema.org,

Note that the schemas of the different record types are not written down
as plain JSON but instead they are directly defined as Python objects,
namely each schema consists of a list required_properties
and of a dict of properties.

The resulting schema that is validated by the code in validate.py is:
{
    'type': 'object',
    'required': required_properties,
    'properties': properties,
    'additionalProperties': False
}

Since schemas are defined as Python objects,
it is possible (and necessary for validate.py) to store regex patterns
as compiled regex expressions.

If you change a schema, make sure that corresponding validation code
is present in validate.py.
"""

import re
from collections import namedtuple

Schema = namedtuple('Schema', ['required_properties', 'properties'])

required_properties = ['type', 'key', 'title', 'year', 'authors']

properties = {}

properties['key'] = {
    'description': 'identifier / (BibTeX) key',
    'type': 'string',
    'pattern': re.compile("""^[0-9]{4}[a-zA-Z]{2,}""")
}

properties['title'] = {
    'description': 'the title of the work',
    'type': 'string',
    'minLength': 6
}

properties['year'] = {
    'description': 'the year of publication (or, if unpublished, the year of creation)',
    'type': 'integer',
    'minimum': 1800,
    'maximum': 2030
}

properties['authors'] = {
    'description': 'the author(s) of the work',
    'type': 'array',
    'items': {
        'description': 'name(s) (and email address) of the author',
        'type': 'object',
        'title': 'author',
        'required': ['last'],
        'properties': {
            'last': {
                'description': "the author's last name",
                'type': 'string',
                'minLength': 2
            },
            'first': {
                'description': "the author's first name(s)",
                'type': 'string',
                'minLength': 2
            },
            'email': {
                'description': "the author's email address",
                'type': 'string',
                'format': 'email'
            }
        },
        'additionalProperties': False
    },
    'minItems': 1,
    'uniqueItems': True
}

properties['doi'] = {
    'description': 'digital object identifier',
    'type': 'string',
    'pattern': re.compile("""(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)""")
    # cf. https://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
}

properties['month'] = {
    'description': 'the month of publication (or, if unpublished, the month of creation)',
    'type': 'integer',
    'minimum': 1,
    'maximum': 12
}

properties['note'] = {
    'description': 'miscellaneous extra information',
    'type': 'string',
    'minLength': 2
}

properties['urls'] = {
    'description': 'URL(s) related to the work',
    'type': 'array',
    'items': {
        'description': 'description of a hyperlink',
        'type': 'object',
        'title': 'URL',
        'required': ['name', 'url'],
        'properties': {
            'name': {
                'description': 'short description of the URL',
                'type': 'string',
                'minLength': 3
            },
            'url': {
                'description': 'URL',
                'type': 'string',
                'format': 'uri',
                'pattern': re.compile("""^(https?|ftp)://""")
            }
        },
        'additionalProperties': False
    },
    'minItems': 1,
    'uniqueItems': True
}

properties['tags'] = {
    'description': 'tags / keywords related to the work',
    'type': 'array',
    'items': {
        'description': 'description of a tag / keyword',
        'type': 'object',
        'title': 'tag',
        'required': ['name'],
        'properties': {
            'name': {
                'description': 'name of the tag',
                'type': 'string',
                'minLength': 2
            },
            'color': {
                'description': "hex. color-code (eg. 'C31F25')",
                'type': 'string',
                'pattern': re.compile("""^[0-9A-F]{6}$""")
            }
        },
        'additionalProperties': False
    },
    'minItems': 1,
    'uniqueItems': True
}

properties['open_access'] = {
    'description': 'marks if the work can be accessed freely',
    'type': 'boolean'
}
"""If `open_access` is set then it must be either `true` or `false`.
Hence for any given record, three different states are possible.
A tag called `open_access` could only destinguish between two states,
which is not useful for making a statistic."""
