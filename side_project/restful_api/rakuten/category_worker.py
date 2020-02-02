#!/usr/bin/env python
import pika
import sys
import time
import socket
import os
import json
import requests
import sys
sys.path.append('/')
from common.downloader import Downloader
from common.rate_limiter import RateLimiter
from common.redis_cache import RedisCache
import pdb
import math


class RakutenCategoryWorker:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        self.search_page_url = 'https://www.rakuten.com.tw/graphql'
        RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
        RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
        RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.ch1 = self.connection.channel()
        self.ch1.queue_declare(queue='rakuten_categories', durable=True)
        self.ch2 = self.connection.channel()
        self.ch2.queue_declare(queue='rakuten_products', durable=True)
        self.product_queue = None
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.fluentd_postgres_category_url = 'http://{}:{}/postgres.{}.category.http'.format(address, fluentd_port, 'rakuten')
        self.search_category_payload = {"operationName":"fetchFacetCategory","variables":{"parameters":{"categoryId":"","searchConjunction":"AND","categoryLevel":1}},"query":"query fetchFacetCategory($parameters: FacetCategoryInputType!) {\n  facetCategory(parameters: $parameters) {\n    facetCategoryList {\n      ...FacetCategoryFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FacetCategoryFragment on SearchPageFacetCategory {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  count\n  __typename\n}\n"}

    def callback(self, ch, method, properties, body):
        category_id, level, is_leaf_node, page_count, name, existed_in_database = json.loads(body)
        if is_leaf_node:
            if not existed_in_database:
                requests.get(self.fluentd_postgres_category_url, json={
                    'id':category_id, 
                    'level':level, 
                    'is_leaf_node':is_leaf_node, 
                    'page_count': page_count, 
                    'name': name
                })
            for page_id in range(1, min(page_count+1, 501)):
                self.product_queue = self.ch2.queue_declare(queue='rakuten_products', durable=True, passive=True)
                while self.product_queue.method.message_count >= 500:
                    time.sleep(10)
                    self.product_queue = self.ch2.queue_declare(queue='rakuten_products', durable=True, passive=True)

                parameters = {"pageNumber":page_id,"categoryId":"{}".format(category_id)}
                self.ch2.basic_publish(
                    exchange='',
                    routing_key='rakuten_products',
                    body=json.dumps(parameters),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))
        else:
            self.search_category_payload['variables']['parameters']['categoryId'] = category_id
            self.search_category_payload['variables']['parameters']['categoryLevel'] = level
            resp = requests.post(self.search_page_url, json=self.search_category_payload)
            api_data = json.loads(resp.text)
            categories = api_data['data']['facetCategory']['facetCategoryList']
            for category in categories:
                row = (category['id'], category['level'], category['isLeafNode'], int(math.ceil(category['count']/20)), category['name'], False) # every page has 20 products
                self.ch1.basic_publish(
                    exchange='',
                    routing_key='rakuten_categories',
                    body=json.dumps(row),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.ch1.basic_qos(prefetch_count=1)
        self.ch1.basic_consume(
            queue='rakuten_categories', on_message_callback=self.callback)
        self.ch1.start_consuming()

if __name__ == '__main__':
    rate_limiter = RateLimiter('rakuten_crawler')
    redis_cache = RedisCache()
    downloader = Downloader(rate_limiter, cache=redis_cache, method='post')
    try:
        rakuten_category_worker = RakutenCategoryWorker(downloader)
        rakuten_category_worker.run()
    except:
        rakuten_category_worker.connection = None
    finally:
        if rakuten_category_worker.connection is not None:
            rakuten_category_worker.connection.close()
