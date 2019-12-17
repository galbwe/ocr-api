from schemas.image_schema import ImageSchema
from .redis_dao import RedisDao


class RedisImageDao(RedisDao):
    def __init__(self, redis_client, uuid_generator, collection='images'):
        schema = ImageSchema()
        super().__init__(redis_client, uuid_generator, schema, collection)
