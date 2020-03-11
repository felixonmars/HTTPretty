import os
import requests
import httpretty

from redis import Redis
from unittest import skipUnless


def redis_available():
    params = dict(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT'))
    )
    conn = Redis(**params)
    try:
        list(conn.keys('*'))
        conn.close()
        return True
    except Exception:
        return False


@skipUnless(redis_available, reason='no redis server available for test')
@httpretty.activate()
def test_work_in_parallel_to_redis():
    "HTTPretty should passthrough redis connections"

    redis = Redis()

    keys = redis.keys('*')
    for key in keys:
        redis.delete(key)

    redis.append('item1', 'value1')
    redis.append('item2', 'value2')


    sorted(redis.keys('*')).should.equal([b'item1', b'item2'])