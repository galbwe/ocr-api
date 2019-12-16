from datetime import datetime

import pytest

from models.image import Image
from models.word_confidence_result import WordConfidenceResult
from models.ocr_result import OcrResult
from utils.uuid_generator import UuidGenerator
from schemas.image_schema import ImageSchema
from schemas.ocr_result_schema import OcrResultSchema
from schemas.word_confidence_result_schema import WordConfidenceResultSchema
from models.image import Image
from models.word_confidence_result import WordConfidenceResult
from models.ocr_result import OcrResult


DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

@pytest.fixture(scope="module")
def redis_data():
    uuid = UuidGenerator()
    image_id = next(uuid)
    ocr_result_id = next(uuid)
    word_confidence_result_id = next(uuid)
    image = {"id": image_id,
            "filename": "license_plate.jpg",
            "date_uploaded": datetime.now().strftime(DATE_FORMAT)}
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
        'date_converted': datetime.now().strftime(DATE_FORMAT)
    }
    return image, ocr_result, word_confidence_result

@pytest.fixture(scope='module')
def application_objects():
    uuid = UuidGenerator()
    image_id = next(uuid)
    ocr_result_id = next(uuid)
    word_confidence_result_id = next(uuid)
    image = Image(image_id, 'license_plate.jpg', datetime.now())
    word_confidence_result = WordConfidenceResult(
        word_confidence_result_id, ocr_result_id, 2, 1, 1, 0, 0, 0, 36, 92, 582,
            269, 96, 'This')
    ocr_result = OcrResult(ocr_result_id, image_id, 'PENDING',
        'The quick brown fox jumped over the sleeping dog.',
        datetime.now())
    return image, word_confidence_result, ocr_result

def test_deserialize_image(redis_data):
    schema = ImageSchema()
    redis_image_data, ocr_result_data, word_confidence_result_data = redis_data
    image = schema.load(redis_image_data)
    assert isinstance(image, Image)
    assert image.id == redis_image_data['id']
    assert image.filename == 'license_plate.jpg'
    assert isinstance(image.date_uploaded, datetime)
    assert image.date_uploaded == datetime.strptime(redis_image_data['date_uploaded'], DATE_FORMAT)


def test_deserialize_word_confidence_result(redis_data):
    schema = WordConfidenceResultSchema()
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
    image_data, ocr_result_data, word_confidence_result_data = redis_data
    ocr_result = schema.load(ocr_result_data)
    assert isinstance(ocr_result, OcrResult)
    assert ocr_result.id == ocr_result_data['id']
    assert ocr_result.image_id == image_data['id']
    assert ocr_result.ocr_conversion_status == 'PENDING'
    assert ocr_result.text == 'The quick brown fox jumped over the sleeping dog.'
    assert ocr_result.date_converted == datetime.strptime(ocr_result_data['date_converted'], DATE_FORMAT)


def test_serialize_image(application_objects):
    image, word_confidence_result, ocr_result = application_objects
    schema = ImageSchema()
    image_data = schema.dump(image)
    assert isinstance(image_data, dict)
    assert image.id == image_data['id']
    assert image.filename == 'license_plate.jpg'
    assert isinstance(image.date_uploaded, datetime)
    assert image.date_uploaded == datetime.strptime(image_data['date_uploaded'], DATE_FORMAT)


def test_serialize_ocr_result(application_objects):
    image, word_confidence_result, ocr_result = application_objects
    schema = OcrResultSchema()
    ocr_result_data = schema.dump(ocr_result)
    assert isinstance(ocr_result_data, dict)
    assert ocr_result.id == ocr_result_data['id']
    assert ocr_result.image_id == image.id
    assert ocr_result.ocr_conversion_status == 'PENDING'
    assert ocr_result.text == 'The quick brown fox jumped over the sleeping dog.'
    assert ocr_result.date_converted == datetime.strptime(ocr_result_data['date_converted'], DATE_FORMAT)


def test_serialize_word_confidence_result(application_objects):
    image, word_confidence_result, ocr_result = application_objects
    schema = WordConfidenceResultSchema()
    word_confidence_result_data = schema.dump(word_confidence_result)
    assert isinstance(word_confidence_result_data, dict)
    assert word_confidence_result.id == word_confidence_result_data['id']
    assert word_confidence_result.ocr_result_id == ocr_result.id
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
