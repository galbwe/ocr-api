from marshmallow import Schema, fields, post_load

from models.ocr_result import OcrResult
from .validation import validate_uuid

class OcrResultSchema(Schema):
    '''
    Schema for converting between OcrResult class and data returned from redis
    client.
    '''
    id = fields.Str(validation=validate_uuid)
    image_id = fields.Str(validation=validate_uuid)
    ocr_conversion_status = fields.Str()
    text = fields.String()
    date_converted = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f")

    @post_load
    def make_ocr_result(self, data, **kwargs):
        id = data['id']
        image_id = data['image_id']
        ocr_conversion_status = data['ocr_conversion_status']
        text = data['text']
        date_converted = data['date_converted']

        return OcrResult(id, image_id, ocr_conversion_status, text,
                         date_converted)
