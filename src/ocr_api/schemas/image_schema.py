from marshmallow import Schema, fields, post_load

from models.image import Image
from .validation import validate_uuid

from utils.uuid_generator import UuidGenerator

class ImageSchema(Schema):
    '''
    Schema for converting between Image class and data returned from redis
    client.
    '''
    id = fields.Str(validation=validate_uuid)
    filename = fields.Str()
    date_uploaded = fields.DateTime('%Y-%m-%d %H:%M:%S.%f')
    ocr_result_id = fields.Str(validation=validate_uuid)

    @post_load
    def make_image(self, data, **kwargs):
        id = data['id']
        filename = data['filename']
        date_uploaded = data['date_uploaded']
        ocr_result_id = data['ocr_result_id']
        return Image(id, filename, date_uploaded, ocr_result_id)
