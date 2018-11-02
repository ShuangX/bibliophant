"""JSON schema for bibliographic records of type article
The main idea is documented in common.py
"""
__all__ = []

from . import common

required_properties = common.required_properties + ["journal"]
# 'volume' might also be considered as a required property!

properties = common.properties.copy()

properties["type"] = {
    "description": "this bibliographic record is of type article",
    "const": "article",
}

properties["journal"] = {
    "description": "the journal or magazine the work was published in",
    "type": "string",
    "minLength": 4,
}

properties["volume"] = {
    "description": "the volume of the journal",
    "type": "string",
    "minLength": 1,
}

properties["number"] = {
    "description": "the '(issue) number' of a journal (this is not the 'article number' assigned by some journals)",
    "type": "string",
    "minLength": 1,
}

properties["pages"] = {
    "description": "page numbers, separated either by commas or double-hyphens",
    "type": "string",
    "minLength": 1,
}

properties["eprint"] = {
    "description": "information for referring to eprints",
    "type": "object",
    "title": "eprint",
    "required": ["eprint"],
    "properties": {
        "eprint": {
            "description": "eprint field (eg. 'hep-ph/9609357' or '0707.3168')",
            "type": "string",
            "minLength": 9,
        },
        "archive_prefix": {
            "description": "for new style arXiv identifiers (eg. 'arXiv')",
            "type": "string",
            "minLength": 5,
        },
        "primary_class": {
            "description": "for new style arXiv identifiers (eg. 'physics.flu-dyn')",
            "type": "string",
            "minLength": 5,
        },
    },
    "additionalProperties": False,
}
# for further information go to https://arxiv.org/hypertex/bibstyles/

properties["abstract"] = {
    "description": "the abstract of the article",
    "type": "string",
    "minLength": 10,
}

schema = common.Schema(required_properties, properties)
