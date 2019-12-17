from datetime import datetime
import json

import pytest

from models.image import Image


def test_get_image_by_id(reset_redis_cache, redis_image_dao, date_format):
    image = redis_image_dao.get_by_id('e42f523c-d919-4dac-85b6-efe850051b85')
    assert isinstance(image, Image)
    assert image.id == 'e42f523c-d919-4dac-85b6-efe850051b85'
    assert image.filename == 'license_plate.jpg'
    assert image.date_uploaded == datetime.strptime('2019-12-15 22:15:07.389647', date_format)
    assert image.ocr_result_id == '70959903-7463-4181-a6a3-1b12c266dbb0'

    non_existant_uuid = 'dd2b9964-6d2f-45c3-9848-7428efd98342'
    with pytest.raises(ValueError):
        bad_image = redis_image_dao.get_by_id(non_existant_uuid)


def test_update_image(reset_redis_cache, redis_image_dao, images, r, date_format):
    image_1, image_2 = images
    image = redis_image_dao.update('e42f523c-d919-4dac-85b6-efe850051b85', image_1)
    data = r.hget('test-images', 'e42f523c-d919-4dac-85b6-efe850051b85')
    image_dict = json.loads(data.decode())
    assert image_dict['id'] == image_1.id
    assert image_dict['filename'] == image_1.filename
    assert image_dict['date_uploaded'] == image_1.date_uploaded.strftime(date_format)
    assert image_dict['ocr_result_id'] == image_1.ocr_result_id
    assert image.id == image_1.id
    assert image == image_1
