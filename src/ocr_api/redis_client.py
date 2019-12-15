import os
import json

from redis import Redis


class RedisClient:
    '''
    Simple client for redis server. The set method accepts strings as keys and
    a dictionary of strings for values.
    '''
    def __init__(self, host=None, port=None):
        self.host = host or os.environ.get('REDIS_HOST', 'localhost')
        self.port = port or os.environ.get('REDIS_PORT', 6379)
        self._r = Redis(self.host, self.port)

    def set(self, key, value):
        string_value = json.dumps(value)
        self._r.set(key, string_value)

    def get(self, key):
        binary_data = self._r.get(key)
        string_data = binary_data.decode()
        return json.loads(string_data)
