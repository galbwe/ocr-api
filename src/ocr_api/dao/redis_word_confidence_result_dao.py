from schemas.word_confidence_result_schema import WordConfidenceResultSchema
from .redis_dao import RedisDao


class RedisWordConfidenceResultDao(RedisDao):

    def __init__(self, redis_client, uuid_generator, collection='word-confidence-results'):
        schema = WordConfidenceResultSchema()
        super().__init__(redis_client, uuid_generator, schema, collection)
