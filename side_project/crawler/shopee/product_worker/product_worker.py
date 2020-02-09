import os 
import sys
import pika
import json
from time import time
import socket
import redis
from common.session_adapter import sess
from common.downloader import Downloader
from common.rate_limiter import RateLimiter
from common.redis_cache import RedisCache
import pdb
import psycopg2
from datetime import datetime

class ProductWorker:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.product_url = 'https://shopee.tw/api/v2/item/get?itemid={}&shopid={}'
        self.fluentd_url = 'http://{}:{}/s3.{}.http'.format(address, fluentd_port, 'shopee')
        self.fluentd_postgres_product_url = 'http://{}:{}/postgres.{}.product.http'.format(address, fluentd_port, 'shopee')

    def callback(self, ch, method, properties, body):
        cur_date = datetime.now().date()
        record = json.loads(body)
        html = self.downloader(self.product_url.format(record['itemid'], record['shopid']))
        try:
            if html is not None:
                api_data = json.loads(html)
                name = api_data['item']['name']
                itemid = api_data['item']['itemid']
                sellerid = api_data['item']['shopid']
                historical_sold = api_data['item']['historical_sold']
                price_max = api_data['item']['price_max']
                price_min = api_data['item']['price_min']
                product = {
                        'date': cur_date.strftime('%Y-%m-%d'),
                        'name': name,
                        'itemid': itemid,
                        'sellerid': sellerid,
                        'historical_sold': historical_sold,
                        'price_max':price_max,
                        'price_min':price_min
                        }
                sess.get(self.fluentd_postgres_product_url, json=product)
                sess.get(self.fluentd_url, json=api_data)
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
        downloader = Downloader(rate_limiter, cache=redis_cache, method='get')
        product_worker = ProductWorker(downloader)
        ch.basic_consume(
                queue='products', on_message_callback=product_worker.callback)
        ch.start_consuming()
    except:
        connection = None
    finally:
        if connection is not None:
            connection.close()
