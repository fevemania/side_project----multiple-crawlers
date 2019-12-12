#!/usr/bin/env python
import pika
import sys
import time
import socket
import os
import json
import requests
from downloader import Downloader
from rate_limiter import RateLimiter
from redis_cache import RedisCache
import pdb

class CategoryWorker:
    def __init__(self, downloader):
        self.downloader = downloader
        self.category_url = 'https://shopee.tw/api/v2/search_items/?by=pop&fe_categoryids={}&limit={}&newest={}'
        self.n_items = 50
        self.offset = 0
        self.ch2 = None
        self.product_queue = None

    def callback(self, ch, method, properties, body):
        row = json.loads(body)
        while True:
            try:
                self.product_queue = self.ch2.queue_declare(queue='products', durable=True, passive=True)
                if self.product_queue.method.message_count >= 500:
                    print(self.product_queue.method.message_count)
                    print('wait')
                    time.sleep(10)
                html = self.downloader(self.category_url.format(row['category_id'], self.n_items, self.offset))
                if html is None:
                    break
                api_data = json.loads(html)
                if api_data['items'] is None:
                    self.offset = 0
                    break
                product = {}
                for i in range(len(api_data['items'])):
                    item = api_data['items'][i]
                    product['category_id'] = row['category_id']
                    product['itemid'] = item['itemid']
                    product['shopid'] = item['shopid']
                    product['name'] = item['name']
                    self.ch2.basic_publish(
                        exchange='',
                        routing_key='products',
                        body=json.dumps(product),
                        properties=pika.BasicProperties(
                            delivery_mode=2,
                        ))
                self.offset += self.n_items
            except Exception as e: 
                print(e)
                print('category callback exception')
        print('good') 
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        try:
            credentials = pika.PlainCredentials('admin', 'mypass')  
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'), credentials=credentials))
            ch1 = connection.channel()
            self.ch2 = connection.channel()
            ch1.queue_declare(queue='categories', durable=True)
            self.ch2.queue_declare(queue='products', durable=True)
            ch1.basic_qos(prefetch_count=1)
            ch1.basic_consume(
                queue='categories', on_message_callback=self.callback)
            ch1.start_consuming()
        except:
            connection = None
        finally:
            if connection is not None:
                connection.close()
#def is_open(ip, port):
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    try:
#        s.connect((ip, int(port)))
#        s.shutdown(2)
#        print('True')
#    except:
#        print('False')

if __name__ == '__main__':
#   is_open(os.environ.get('RABBIT_HOST'), 5672)
    rate_limiter = RateLimiter()
    redis_cache = RedisCache()
    downloader = Downloader(rate_limiter, cache=redis_cache, timeout=300)
    category_worker = CategoryWorker(downloader)
    category_worker.run()
    
