import redis
import time
import os

class RateLimiter:
    def __init__(self, port=6379, rate_limit_per_second=30):
        self.r = redis.StrictRedis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0)
        self.rate_limit_per_second = rate_limit_per_second

    def wait(self):
        ts = time.time()
        keyname = str(int(ts))
        num_requests = self.r.get(keyname)
        while num_requests:
            if num_requests and int(num_requests) <= self.rate_limit_per_second:
                break
            num_requests = self.r.get(keyname)
        pipe = self.r.pipeline()
        pipe.incr(keyname)
        pipe.expire(keyname, 1)
        pipe.execute()
