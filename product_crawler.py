import os 
import sys
import pika
import requests
import json
from time import time
from pprint import pprint
import socket
import redis
from downloader import Downloader
from rate_limiter import RateLimiter
from redis_cache import RedisCache

class ProductCrawler:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'locahost'))
        self.product_url = 'https://shopee.tw/api/v2/item/get?itemid={}&shopid={}'
        self.fluentd_url = 'http://{}:{}/mysql.access'.format(address, fluentd_port)

    def callback(self, ch, method, properties, body):
        product = json.loads(body)
        html = self.downloader(self.product_url.format(product['itemid'], product['shopid']))
        if html is not None:
            api_data = json.loads(html)
            product['price_min'] = api_data['item']['price_min'] / 100000
            product['price_max'] = api_data['item']['price_max'] / 100000
            requests.get(self.fluentd_url, json=product)    
            ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    try:
        credentials = pika.PlainCredentials('admin', 'mypass')
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'), credentials=credentials))
        ch = connection.channel()
        ch.queue_declare(queue='products', durable=True)
        ch.basic_qos(prefetch_count=1)
        rate_limiter = RateLimiter()
        redis_cache = RedisCache()
        downloader = Downloader(rate_limiter, cache=redis_cache)
        product_crawler = ProductCrawler(downloader)
        ch.basic_consume(
                queue='products', on_message_callback=product_crawler.callback)
        ch.start_consuming()
    except:
        connection = None 
    finally:
        if connection is not None:
            connection.close()