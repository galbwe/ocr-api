from models.image import Image


class RedisImageDao:
    def __init__(self, redis_client, image_schema, uuid_generator, collection='images'):
        self.redis_client = redis_client
        self.image_schema = image_schema
        self.uuid_generator = uuid_generator
        self.collection = collection

    def get_image_by_id(self, id):
        if self.redis_client.collection_has_key(self.collection, id):
            image_data = self.redis_client.get(id)
            return self.image_schema.load(image_data)
        raise ValueError('Collection {self.collection} has no key {id}.')

    def update_image(self, id, image):
        if self.redis_client.collection_has_key(self.collection, id):
            image.id = id
            image_data = self.image_schema.dump(image)
            self.redis_client.set(id, image_data)
            return image
        raise ValueError(f'Collection {self.collection} has no key {id}.')

    def delete_image(self, id):
        if self.redis_client.collection_has_key(self.collection, key):
            image_data = self.redis_client.get(key)
            self.redis_client.delete(key)
            return self.image_schema.load(image_data)
        raise ValueError(f'Collection {self.collection} has no key {id}.')

    def insert_image(self, image):
        id = next(self.uuid_generator)
        while not self.redis_client.collection_has_key(self.collection, id):
            id = next(self.uuid_generator)
        image.id = id
        image_data = self.image_schema.dump(image)
        self.redis_client.set(key, image_data)
        return image

    def get_all_image_ids(self):
        return self.redis_client.hkeys(self.collection)
