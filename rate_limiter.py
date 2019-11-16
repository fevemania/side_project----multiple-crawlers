import redis
import time
import os

class RateLimiter:
    def __init__(self, port=6379, rate_limit_per_second=1):
        self.r = redis.StrictRedis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0)
        self.rate_limit_per_second = rate_limit_per_second

    def wait(self):
        ts = time.time()
        keyname = str(int(ts/10))
        while self.r.get(keyname) and int(self.r.get(keyname)) > self.rate_limit_per_second: pass
        pipe = self.r.pipeline()
        pipe.incr(keyname)
        pipe.expire(keyname, 10)
        pipe.execute()
