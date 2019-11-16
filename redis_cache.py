from datetime import datetime, timedelta
from redis import StrictRedis
import json
import os

class RedisCache:
    def __init__(self, expires=timedelta(days=1), encoding='utf-8'):
        self.client = StrictRedis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0)
        self.expires = expires
        self.encoding = encoding

    def __getitem__(self, url):
        record = self.client.get(url)
        if record:
            return json.loads(record.decode(self.encoding))
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        data = bytes(json.dumps(result), self.encoding)
        self.client.setex(url, self.expires, data)
