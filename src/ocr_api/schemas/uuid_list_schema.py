from marshmallow import Schema, fields, validates, post_dump, pre_dump, pre_load, post_load

from .validation import validate_uuid

class UUIDListSchema(Schema):
    uuids = fields.List(fields.String())

    # dumping = serializing = application object -> raw object
    # loading = deserializing = raw object -> application object
    # application object is a list of strings
    # raw object is also a list of strings
    @pre_dump
    @pre_load
    def add_envelope(self, data, **kwargs):
        return {'uuids': data}

    @post_dump
    @post_load
    def remove_envelope(self, data, **kwargs):
        return data['uuids']

    @validates('uuids')
    def validate_uuids(self, uuids):
        for uuid in uuids:
            validate_uuid(uuid)
