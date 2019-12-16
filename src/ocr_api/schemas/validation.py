import re

from marshmallow import ValidationError

UUID_REGEX = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

def validate_uuid(id):
    if not isinstance(id, str):
        raise ValidationError('UUID must be of type string')
    if len(id) != 36:
        raise ValidationError('UUID must be of length 36.')
    if not re.match(UUID_REGEX, id):
        raise ValidationError('Incorrect format for UUID.')
