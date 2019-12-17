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


def test_delete_image(reset_redis_cache, redis_image_dao, r, date_format):
    deleted_image = redis_image_dao.delete('e42f523c-d919-4dac-85b6-efe850051b85')
    assert not r.hexists('test-images', 'e42f523c-d919-4dac-85b6-efe850051b85')
    assert deleted_image.id == 'e42f523c-d919-4dac-85b6-efe850051b85'
    assert deleted_image.filename == 'license_plate.jpg'
    assert deleted_image.date_uploaded.strftime(date_format) == '2019-12-15 22:15:07.389647'
    assert deleted_image.ocr_result_id == '70959903-7463-4181-a6a3-1b12c266dbb0'

    with pytest.raises(ValueError):
        bad_delete = redis_image_dao.delete('jaberwocky')


def test_insert_image(reset_redis_cache, redis_image_dao, images, r, date_format):
    image_1, image_2 = images
    inserted_image = redis_image_dao.insert(image_1)
    assert inserted_image == image_1
    assert inserted_image.id == image_1.id
    assert r.hlen('test-images') == 3

    with pytest.raises(ValueError):
        another_inserted_image = redis_image_dao.insert(image_1)


def test_get_all_images(reset_redis_cache, redis_image_dao, date_format):
    images = redis_image_dao.get_all()
    assert images[0] == Image(**{
        'id': 'e42f523c-d919-4dac-85b6-efe850051b85',
        'filename': 'license_plate.jpg',
        'date_uploaded': '2019-12-15 22:15:07.389647',
        'ocr_result_id': '70959903-7463-4181-a6a3-1b12c266dbb0'
    })
    assert images[0].id == 'e42f523c-d919-4dac-85b6-efe850051b85'
    assert images[1] == Image(**{
        'id': '0ba0b98f-d5e3-42a9-9c38-8081e4f9883f',
        'filename': 'license_plate.png',
        'date_uploaded': '2019-12-15 22:15:08.223109',
        'ocr_result_id': '1858da11-6b30-472c-9280-79ca157cb4ca'
    })
    assert images[1].id == '0ba0b98f-d5e3-42a9-9c38-8081e4f9883f'
