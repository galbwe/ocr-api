from datetime import datetime
import json

import pytest
from redis import Redis

from utils.uuid_generator import UuidGenerator
from redis_client import RedisClient
from dao.redis_image_dao import RedisImageDao
from models.image import Image


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
