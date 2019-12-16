from marshmallow import Schema, fields, post_load

from models.ocr_result import OcrResult
from .validation import validate_uuid
from .uuid_list_schema import UUIDListSchema

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
    word_confidence_result_ids = fields.Nested(UUIDListSchema)

    @post_load
    def make_ocr_result(self, data, **kwargs):
        id = data['id']
        image_id = data['image_id']
        ocr_conversion_status = data['ocr_conversion_status']
        text = data['text']
        date_converted = data['date_converted']
        word_confidence_result_ids = data['word_confidence_result_ids']

        return OcrResult(id, image_id, ocr_conversion_status, text,
                         date_converted, word_confidence_result_ids)
