import pika
import os 
import sys
from datetime import datetime
import json
from time import time
import socket
import redis
from common.session_adapter import sess
from common.downloader import Downloader
from common.rate_limiter import RateLimiter
from common.redis_cache import RedisCache
import pdb
from datetime import timedelta
import psycopg2
from datetime import datetime

RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')

class PinkoiProductWorker:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.fluentd_s3_url = 'http://{}:{}/s3.{}.http'.format(address, fluentd_port, 'pinkoi')
        self.fluentd_postgres_url = 'http://{}:{}/postgres.{}.http'.format(address, fluentd_port, 'pinkoi')
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='pinkoi_products', durable=True)

    def callback(self, ch, method, properties, body):
        cur_date = datetime.now().date()
        url = json.loads(body)
        html = self.downloader(url)
        api_data = json.loads(html)
        product_list = api_data['result'][0]['hits']['hits']
        if product_list:
            sess.get(self.fluentd_s3_url, json=product_list)
            product_data = []
            for product in product_list:
                product_data.append({
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'currency': product['fields']['currency']['name'],
                    'price': product['fields']['price'],
                    'name': product['fields']['title']
                })
            sess.get(self.fluentd_postgres_url, json=product_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='pinkoi_products', on_message_callback=self.callback)
        self.channel.start_consuming()

if __name__ == '__main__':
    rate_limiter = RateLimiter('pinkoi_crawler')
    redis_cache = RedisCache()
    downloader = Downloader(rate_limiter, cache=redis_cache, method='get')
    try:
        pinkoi_product_worker = PinkoiProductWorker(downloader)
        pinkoi_product_worker.run()
    except:
        pinkoi_product_worker.connection = None
    finally:
        if pinkoi_product_worker.connection is not None:
            pinkoi_product_worker.connection.close()

