"""JSON schema validation

Note that only the validation keywords defined at json-schema.org,
which are required by the application are implemented.
If you change the schema then it might be necessary to extend this module.

Note also that it is assumed that the schema is correct.
The module only validates the data against the schema.
Usually it is not actively checked if the schema makes sense (cf. SchemaError).
"""

import importlib
import re

string_format_patterns = {}
string_format_patterns['uri'] = re.compile(r"^\w+:(\/?\/?)[^\s]+$")
string_format_patterns['email'] = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class ValidationError(Exception):
    """raised if JSON data does not fit the schema"""
    pass


class SchemaError(Exception):
    """raised if the JSON schema contains conditions which were not validated,
    either because the schema is wrong,
    or the validation code is incomplete or incorrect.
    """
    pass


def validate_record(record):
    if not isinstance(record, dict):
        raise ValidationError('record is not a dict (JSON object)')

    try:
        record_type = record['type']
    except KeyError:
        raise ValidationError("record has no 'type' property")

    try:
        record_type_module = importlib.import_module(record_type)
        schema = record_type_module.schema
    except:
        raise ValidationError(f"record type {record_type} is not defined")

    if not all((prop in record) for prop in schema.required_properties):
        raise ValidationError(f'record must contain all required_properties {required_properties}')

    record_property_names = set(record.keys())

    for prop_name in schema.properties.keys():
        if prop_name == 'type':
            record_property_names.remove('type')
            continue  # already checked
        if prop_name in record_property_names:
            record_property_names.remove(prop_name)
            prop_schema = schema.properties[prop_name]
            prop_data = record[prop_name]
            validate_property(prop_name, prop_schema, prop_data)

    if record_property_names:
        raise ValidationError(f"record {record['key']} contains properties {record_property_names} which are not specified by the schema in {record_type}.py")


def validate_property(prop_name, prop_schema, prop_data):
    prop_type = prop_schema['type']

    conditions = set(prop_schema.keys()) - {'type', 'description'}

    if prop_type == 'integer':
        if not isinstance(prop_data, int):
            raise ValidationError(f"{prop_name} must be an integer")

        if 'minimum' in prop_schema:
            conditions.remove('minimum')
            if prop_data < prop_schema['minimum']:
                raise ValidationError(f"{prop_name} must not be smaller than {prop_schema['minimum']}")

        if 'maximum' in prop_schema:
            conditions.remove('maximum')
            if prop_data > prop_schema['maximum']:
                raise ValidationError(f"{prop_name} must not be larger than {prop_schema['maximum']}")

    elif prop_type == 'string':
        if not isinstance(prop_data, str):
            raise ValidationError(f'{prop_name} must be a string')

        if 'minLength' in prop_schema:
            conditions.remove('minLength')
            if len(prop_data) < prop_schema['minLength']:
                raise ValidationError(f"{prop_name} must not be shorter than {prop_schema['minLength']}")

        if 'maxLength' in prop_schema:
            conditions.remove('maxLength')
            if len(prop_data) > prop_schema['maxLength']:
                raise ValidationError(f"{prop_name} must not be larger than {prop_schema['maxLength']}")

        if 'pattern' in prop_schema:
            conditions.remove('pattern')
            if not prop_schema['pattern'].search(prop_data):
                raise ValidationError(f"{prop_name} did not match the specified pattern {prop_schema['pattern'].pattern}")

        if 'format' in prop_schema:
            conditions.remove('format')
            if prop_schema['format'] == 'uri':
                if not string_format_patterns['uri'].search(prop_data):
                    raise ValidationError(f"{prop_name} did not match the URI format")
            elif prop_schema['format'] == 'email':
                if not string_format_patterns['email'].search(prop_data):
                    raise ValidationError(f"{prop_name} did not match the email format")
            else:
                raise SchemaError(f"the string format {prop_schema['format']} is not defined or implemented")

    elif prop_type == 'boolean':
        if not isinstance(prop_data, bool):
            raise ValidationError(f'{prop_name} must be a boolean')

    elif prop_type == 'array':
        if not isinstance(prop_data, list):
            raise ValidationError(f'{prop_name} must be a list (JSON array)')

        if 'minItems' in prop_schema:
            conditions.remove('minItems')
            if len(prop_data) < prop_schema['minItems']:
                raise ValidationError(f"{prop_name} must contain at least {prop_schema['minItems']} items")

        if 'uniqueItems' in prop_schema:
            conditions.remove('uniqueItems')
            if prop_schema['uniqueItems']:
                if len(prop_data) > len(set(str(tag) for tag in prop_data)):
                    raise ValidationError(f"the items in {prop_name} must be unique")

        if 'items' in prop_schema:
            conditions.remove('items')
            item_schema = prop_schema['items']
            for item in prop_data:
                validate_property(f"{prop_name} item", item_schema, item)

    elif prop_type == 'object':
        if not isinstance(prop_data, dict):
            raise ValidationError(f"{prop_name} is not a dict (JSON object)")

        conditions = conditions - {'title', 'properties'}

        if 'required' in prop_schema:
            conditions.remove('required')
            if not all((prop in prop_data) for prop in prop_schema['required']):
                raise ValidationError(f"{prop_schema['title']} must contain all required_properties {prop_schema['required']}")

        object_property_names = set(prop_data.keys())

        for obj_prop_name in prop_schema['properties'].keys():
            if obj_prop_name in object_property_names:
                object_property_names.remove(obj_prop_name)
                obj_prop_schema = prop_schema['properties'][obj_prop_name]
                obj_prop_data = prop_data[obj_prop_name]
                validate_property(obj_prop_name, obj_prop_schema, obj_prop_data)

        if 'additionalProperties' in prop_schema:
            conditions.remove('additionalProperties')
            if prop_schema['additionalProperties'] is False and object_property_names:
                raise ValidationError(f"{prop_schema['title']} contains properties {object_property_names} which are not specified by the schema")

    else:
        raise SchemaError(f"the property of type {prop_type} is not defined or implemented")

    if conditions:
        raise SchemaError(f"the conditions {conditions} could not be validated")
