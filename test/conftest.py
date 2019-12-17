from datetime import datetime
import json

import pytest
from redis import Redis

from utils.uuid_generator import UuidGenerator
from redis_client import RedisClient
from dao.redis_image_dao import RedisImageDao
from models.image import Image
from models.ocr_result import OcrResult
from models.word_confidence_result import WordConfidenceResult


DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

@pytest.fixture(scope='module')
def date_format():
    global DATE_FORMAT
    return DATE_FORMAT


@pytest.fixture(scope='module')
def r():
    return Redis(host='localhost', db=1)

@pytest.fixture(scope='function')
def reset_redis_cache():
    r = Redis(host='localhost', db=1)
    r.flushdb()
    r.hmset('test-images', {
        'e42f523c-d919-4dac-85b6-efe850051b85': json.dumps({
            'id': 'e42f523c-d919-4dac-85b6-efe850051b85',
            'filename': 'license_plate.jpg',
            'date_uploaded': '2019-12-15 22:15:07.389647',
            'ocr_result_id': '70959903-7463-4181-a6a3-1b12c266dbb0'
        }),
        '0ba0b98f-d5e3-42a9-9c38-8081e4f9883f': json.dumps({
            'id': '0ba0b98f-d5e3-42a9-9c38-8081e4f9883f',
            'filename': 'license_plate.png',
            'date_uploaded': '2019-12-15 22:15:08.223109',
            'ocr_result_id': '1858da11-6b30-472c-9280-79ca157cb4ca'
        })
    })


@pytest.fixture(scope="module")
def redis_image_dao():
    redis_client = RedisClient(host='localhost', db=1)
    uuid_generator = UuidGenerator()
    return RedisImageDao(redis_client, uuid_generator, collection='test-images')


@pytest.fixture(scope="function")
def images():
    return (
        Image(
            id='493f944a-ad5c-4331-a5ff-15dc117ea19f',
            filename='license_plate.bmp',
            date_uploaded=datetime.strptime('2019-12-15 22:15:08.810219', DATE_FORMAT),
            ocr_result_id='c106bbaa-5157-45ed-8c37-3532b9a5676f'
        ),
        Image(
            id='314c223d-5882-458c-952a-72c7e3e8b3ad',
            filename='license_plate.tiff',
            date_uploaded=datetime.strptime('2019-12-15 22:15:09.417252', DATE_FORMAT),
            ocr_result_id='34ed7f5f-e145-4acf-b275-9ff760b6b9e8'
        )
    )


@pytest.fixture(scope="module")
def redis_data():
    uuid = UuidGenerator()
    image_id = next(uuid)
    ocr_result_id = next(uuid)
    word_confidence_result_id = next(uuid)
    image = {"id": image_id,
            "filename": "license_plate.jpg",
            "date_uploaded": datetime.now().strftime(DATE_FORMAT),
            "ocr_result_id": ocr_result_id}
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
        'date_converted': datetime.now().strftime(DATE_FORMAT),
        'word_confidence_result_ids': [word_confidence_result_id]
    }
    return image, ocr_result, word_confidence_result


@pytest.fixture(scope='module')
def application_objects():
    uuid = UuidGenerator()
    image_id = next(uuid)
    ocr_result_id = next(uuid)
    word_confidence_result_id = next(uuid)
    image = Image(image_id, 'license_plate.jpg', datetime.now(), word_confidence_result_id)
    word_confidence_result = WordConfidenceResult(
        word_confidence_result_id, ocr_result_id, 2, 1, 1, 0, 0, 0, 36, 92, 582,
            269, 96, 'This')
    ocr_result = OcrResult(ocr_result_id, image_id, 'PENDING',
        'The quick brown fox jumped over the sleeping dog.',
        datetime.now(), [word_confidence_result_id])
    return image, word_confidence_result, ocr_result
