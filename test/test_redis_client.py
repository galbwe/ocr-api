import pytest
import json
from redis import Redis

from redis_client import RedisClient


def test_hexists(reset_redis_cache):
    client = RedisClient(host='localhost', db=1)
    assert client._r.hexists('test-images', 'e42f523c-d919-4dac-85b6-efe850051b85')
    assert client.collection_has_key('test-images', 'e42f523c-d919-4dac-85b6-efe850051b85')
    assert client.collection_has_key('test-images', '0ba0b98f-d5e3-42a9-9c38-8081e4f9883f')
    assert not client.collection_has_key('test-images', 'abc0deff-d5e3-42a9-9c38-8081e4f9883f')
