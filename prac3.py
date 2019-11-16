import redis
from time import time
import os

r = redis.StrictRedis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0)

print(r.keys())
