import redis
from time import time

class RateLimiter:
    def __init__(self, host='redis', port=6379, rate_limit_per_second=3):
        self.r = redis.StrictRedis(host=host, port=port, db=0)
        self.rate_limit_per_second = rate_limit_per_second

    def check():
        ts = time()
        keyname = str(int(ts/20))
        num_requests = self.r.get(keyname)
        if num_requests and int(num_requests) > self.rate_limit_per_second:
            print('too many requests')
            return False
        else:
            pipe = self.r.pipeline()
            pipe.incr(keyname)
            pipe.expire(keyname, 20)
            pipe.execute()
            return True
