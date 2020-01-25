import os 
import sys
import pika
import requests
import json
from time import time
import socket
import redis
from downloader import Downloader
from rate_limiter import RateLimiter
from redis_cache import RedisCache
import pdb
import psycopg2

class ProductCrawler:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.product_url = 'https://shopee.tw/api/v2/item/get?itemid={}&shopid={}'
        self.fluentd_url = 'http://{}:{}/s3.http.access'.format(address, fluentd_port)

    def callback(self, ch, method, properties, body):
        record = json.loads(body)
        html = self.downloader(self.product_url.format(record['itemid'], record['shopid']))
        try:
            if html is not None:
                api_data = json.loads(html)
                requests.get(self.fluentd_url, json=api_data)
            else:
                print('Oh no')
                print('product html is None')
        except Exception as e:
            print(e)
            print('product callback exception')

        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    try:
        RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
        RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
        RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        ch = connection.channel()
        ch.queue_declare(queue='products', durable=True)
        ch.basic_qos(prefetch_count=1)
        rate_limiter = RateLimiter('shopee_crawler')
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
