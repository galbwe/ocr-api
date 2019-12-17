

class RedisDao:

    def __init__(self, redis_client, uuid_generator, schema, collection):
        self.redis_client = redis_client
        self.uuid_generator = uuid_generator
        self.schema = schema
        self.collection = collection

    def get_by_id(self, id):
        if self.redis_client.collection_has_key(self.collection, id):
            data = self.redis_client.hget(self.collection, id)
            return self.schema.load(data)
        raise ValueError('Collection {self.collection} has no key {id}.')

    def update(self, id, model):
        if self.redis_client.collection_has_key(self.collection, id):
            model.id = id
            data = self.image_schema.dump(model)
            self.redis_client.hset(self.collection, id, data)
            return model
        raise ValueError(f'Collection {self.collection} has no key {id}.')

    def delete(self, id):
        if self.redis_client.collection_has_key(self.collection, id):
            data = self.redis_client.hget(self.collection, id)
            self.redis_client.hdel(self.collection, id)
            return self.schema.load(data)
        raise ValueError(f'Collection {self.collection} has no key {id}.')

    def insert(self, model):
        id = next(self.uuid_generator)
        while self.redis_client.collection_has_key(self.collection, id):
            id = next(self.uuid_generator)
        model.id = id
        data = self.schema.dump(model)
        self.redis_client.hset(self.collection, id, data)
        return model

    def get_all_ids(self):
        return self.redis_client.hkeys(self.collection)
