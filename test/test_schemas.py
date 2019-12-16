from datetime import datetime

import pytest

from utils.uuid_generator import UuidGenerator
from schemas.image_schema import ImageSchema
from schemas.ocr_result_schema import OcrResultSchema
from schemas.word_confidence_result_schema import WordConfidenceResultSchema
from models.image import Image
from models.word_confidence_result import WordConfidenceResult
from models.ocr_result import OcrResult


@pytest.fixture(scope="module")
def redis_data():
    uuid = UuidGenerator()
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    image_id = next(uuid)
    ocr_result_id = next(uuid)
    word_confidence_result_id = next(uuid)
    image = {"id": image_id,
            "filename": "license_plate.jpg",
            "date_uploaded": datetime.now().strftime(fmt)}
    word_confidence_result = {
        'id': word_confidence_result_id,
        'ocr_result_id': ocr_result_id,
        'level': 2,
        'page_num': 1,
        'block_num': 1,
        'par_num': 0,
        'line_num': 0,
        'word_num': 0,
        'left': 36,
        'top': 92,
        'width': 582,
        'height': 269,
        'conf': 96,
        'text': 'This'
    }
    ocr_result = {
        'id': ocr_result_id,
        'image_id': image_id,
        'ocr_conversion_status': 'PENDING',
        'text': 'The quick brown fox jumped over the sleeping dog.',
        'date_converted': datetime.now().strftime(fmt)
    }
    return image, ocr_result, word_confidence_result

def test_deserialize_image(redis_data):
    schema = ImageSchema()
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    redis_image_data, ocr_result_data, word_confidence_result_data = redis_data
    image = schema.load(redis_image_data)
    assert isinstance(image, Image)
    assert image.id == redis_image_data['id']
    assert image.filename == 'license_plate.jpg'
    assert isinstance(image.date_uploaded, datetime)
    assert image.date_uploaded == datetime.strptime(redis_image_data['date_uploaded'], fmt)


def test_deserialize_word_confidence_result(redis_data):
    schema = WordConfidenceResultSchema()
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    redis_image_data, ocr_result_data, word_confidence_result_data = redis_data
    word_confidence_result = schema.load(word_confidence_result_data)
    assert isinstance(word_confidence_result, WordConfidenceResult)
    assert word_confidence_result.id == word_confidence_result_data['id']
    assert word_confidence_result.ocr_result_id == ocr_result_data['id']
    assert word_confidence_result.level == 2
    assert word_confidence_result.page_num == 1
    assert word_confidence_result.block_num == 1
    assert word_confidence_result.par_num == 0
    assert word_confidence_result.line_num == 0
    assert word_confidence_result.left == 36
    assert word_confidence_result.top == 92
    assert word_confidence_result.width == 582
    assert word_confidence_result.height == 269
    assert word_confidence_result.conf == 96
    assert word_confidence_result.text == 'This'


def test_deserialize_ocr_result(redis_data):
    schema = OcrResultSchema()
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    image_data, ocr_result_data, word_confidence_result_data = redis_data
    ocr_result = schema.load(ocr_result_data)
    assert isinstance(ocr_result, OcrResult)
    assert ocr_result.id == ocr_result_data['id']
    assert ocr_result.image_id == image_data['id']
    assert ocr_result.ocr_conversion_status == 'PENDING'
    assert ocr_result.text == 'The quick brown fox jumped over the sleeping dog.'
    assert ocr_result.date_converted == datetime.strptime(ocr_result_data['date_converted'], fmt)
