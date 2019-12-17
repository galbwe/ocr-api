import json

import pytest
from redis import Redis
from datetime import datetime

from models.image import Image
from dao.redis_image_dao import RedisImageDao
from redis_client import RedisClient
from utils.uuid_generator import UuidGenerator


DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def test_get_image_by_id(reset_redis_cache, redis_image_dao):
    image = redis_image_dao.get_by_id('e42f523c-d919-4dac-85b6-efe850051b85')
    assert isinstance(image, Image)
    assert image.id == 'e42f523c-d919-4dac-85b6-efe850051b85'
    assert image.filename == 'license_plate.jpg'
    assert image.date_uploaded == datetime.strptime('2019-12-15 22:15:07.389647', DATE_FORMAT)
    assert image.ocr_result_id == '70959903-7463-4181-a6a3-1b12c266dbb0'

    non_existant_uuid = 'dd2b9964-6d2f-45c3-9848-7428efd98342'
    with pytest.raises(ValueError):
        bad_image = redis_image_dao.get_by_id(non_existant_uuid)
