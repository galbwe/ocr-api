from schemas.ocr_result_schema import OcrResultSchema
from .redis_dao import RedisDao


class OcrResultDao(RedisDao):

    def __init__(self, redis_client, uuid_generator, collection='ocr-results'):
        schema = OcrResultSchema()
        super().__init__(redis_client, uuid_generator, schema, collection)
