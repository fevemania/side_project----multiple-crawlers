import redis
from time import time
import os

r = redis.StrictRedis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0)
ts = time()
keyname = str(int(ts/20))
pipe = r.pipeline()
pipe.incr(keyname)
pipe.expire(keyname, 20)
pipe.execute()

print(r.get(keyname))
