"""JSON schema for bibliographic records of type book
The main idea is documented in common.py
"""
__all__ = []

from . import common

required_properties = common.required_properties + ["publisher"]

properties = common.properties.copy()

properties["type"] = {
    "description": "this bibliographic record is of type book",
    "const": "book",
}

properties["publisher"] = {
    "description": "the publisher of the work",
    "type": "object",
    "title": "publisher",
    "required": ["name"],
    "properties": {
        "name": {
            "description": "name of the publisher",
            "type": "string",
            "minLength": 4,
        },
        "address": {
            "description": "address of the publisher (usually only city)",
            "type": "string",
            "minLength": 4,
        },
    },
    "additionalProperties": False,
}

properties["volume"] = {
    "description": "the volume of a multi-volume book",
    "type": "string",
    "minLength": 1,
}

properties["edition"] = {
    "description": """the edition of a book ("First" or "Second")""",
    "type": "string",
    "minLength": 1,
}

properties["series"] = {
    "description": "the series of books the book was published in",
    "type": "string",
    "minLength": 3,
}

schema = common.Schema(required_properties, properties)
