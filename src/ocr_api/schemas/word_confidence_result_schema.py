from marshmallow import Schema, fields, post_load

from models.word_confidence_result import WordConfidenceResult
from .validation import validate_uuid

class WordConfidenceResultSchema(Schema):
    id = fields.String(validation=validate_uuid)
    ocr_result_id = fields.String(validation=validate_uuid)
    level = fields.Integer()
    page_num = fields.Integer()
    block_num = fields.Integer()
    par_num = fields.Integer()
    line_num = fields.Integer()
    word_num = fields.Integer()
    left = fields.Integer()
    top = fields.Integer()
    width = fields.Integer()
    height = fields.Integer()
    conf = fields.Integer()
    text = fields.String()

    @post_load
    def make_word_confidence_result(self, data, **kwargs):
        return WordConfidenceResult(
            data['id'],
            data['ocr_result_id'],
            data['level'],
            data['page_num'],
            data['block_num'],
            data['par_num'],
            data['line_num'],
            data['word_num'],
            data['left'],
            data['top'],
            data['width'],
            data['height'],
            data['conf'],
            data['text']
        )
