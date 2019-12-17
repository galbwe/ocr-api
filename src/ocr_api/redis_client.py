import os
import json

from redis import Redis


class RedisClient:
    '''
    Simple client for redis server. The set method accepts strings as keys and
    a dictionary of strings for values.
    '''
    def __init__(self, host=None, port=None, db=0):
        self.host = host or os.environ.get('REDIS_HOST', 'localhost')
        self.port = port or os.environ.get('REDIS_PORT', 6379)
        self.db = db
        self._r = Redis(self.host, self.port, db=self.db)

    def set(self, key, value):
        string_value = json.dumps(value)
        self._r.set(str(key), string_value)

    def get(self, key):
        binary_data = self._r.get(key)
        string_data = binary_data.decode()
        return json.loads(string_data)

    def hset(self, collection, key, value):
        string_value = json.dumps(value)
        self._r.hset(collection, str(key), string_value)

    def hget(self, collection, key):
        binary_data = self._r.hget(collection, key)
        string_data = binary_data.decode()
        return json.loads(string_data)

    def hexists(self, collection, key):
        return self._r.hexists(collection, key)

    def delete(self, key):
        self._r.delete(key)

    def key_exists(self, key):
        return self._r.exists(key) > 0

    def hkeys(self, hash):
        binary_keys = self._r.hkeys(hash)
        return [key.decode() for key in binary_keys]

    def collection_has_key(self, collection, key):
        return self._r.hexists(collection, key)
