import redis
from time import time
import os
from minio import Minio
from minio.error import ResponseError
import json
import io
import urllib3
from bs4
https://shopee.tw/api/v2/item/get_ratings?filter=0&flag=1&itemid=2620674592&limit=6&offset=6&shopid=149778783

#minio_cli = Minio('play.min.io', access_key='minio', secret_key='minio123',
#        secure=True)

#product = {'product_id': 25679461, 'product_name': '【附發票】大量現貨不用等Dream time自訂版🌸闆娘實穿❤️綁帶鬆緊激瘦 九分寬褲 高腰 綁帶寬褲 大尺','category_id': 62, 'price_min': 100.0, 'price_max': 100.0}
#product = [25679461,'【附發票】大量現貨不用等Dream time自訂版🌸闆娘實穿❤️綁帶鬆緊激瘦 九分寬褲 高腰 綁帶寬褲 大尺', 100.0, 100.0, 62]
#value = "Some text I want to upload"
#value_as_bytes = value.encode('utf-8')
#value_as_a_stream = io.BytesIO(value_as_bytes)
#minio_cli.put_object('mybucket', 'myobject.csv', value_as_a_stream, len(value_as_bytes))

#import pymysql

#conn = pymysql.connect(host='localhost', user='root', passwd='mypass', db='mysql', charset='utf8mb4')
#cur = conn.cursor()
#cur.execute('USE db')
#sql = 'INSERT INTO products (product_id, product_name, price_min, price_max, category_id) VALUES (%s, %s, %s, %s, %s)'
#cur.execute(sql, product)
#conn.commit()
#cur.close()
#conn.close()
