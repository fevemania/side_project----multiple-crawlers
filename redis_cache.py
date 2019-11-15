from datetime import datetime, timedelta
from redis import StrictRedis
import json

class RedisCache:
    def __init__(self, expires=timedelta(seconds=1), encoding='utf-8'):
        self.client = StrictRedis(host='redis', port=6379, db=0)
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
