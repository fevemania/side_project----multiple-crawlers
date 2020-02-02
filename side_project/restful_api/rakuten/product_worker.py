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
import math
from datetime import datetime


class RakutenProductWorker:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        self.search_page_url = 'https://www.rakuten.com.tw/graphql'
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.fluentd_s3_url = 'http://{}:{}/s3.{}.http'.format(address, fluentd_port, 'rakuten')
        self.fluentd_postgres_product_url = 'http://{}:{}/postgres.{}.product.http'.format(address, fluentd_port, 'rakuten')

        RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
        RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
        RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.ch = self.connection.channel()
        self.ch.queue_declare(queue='rakuten_products', durable=True)
        self.category_queue = None
        self.product_queue = None
        self.search_page_payload = {
                "operationName":"fetchSearchPageResults",
                "variables":{"parameters":{}},
                "query":"query fetchSearchPageResults($parameters: SearchInputType!) {\n  searchPage(parameters: $parameters) {\n    serializedKey\n    title\n    result {\n      abTestVariation\n      items {\n        ...SearchResultItemFragment\n        __typename\n      }\n      totalItems\n      conjunction\n      __typename\n    }\n    recommendationRefItem {\n      shopId\n      itemId\n      rakutenCategoryTree\n      __typename\n    }\n    pagination {\n      itemsPerPage\n      pageNumber\n      totalItems\n      __typename\n    }\n    currentCategoryInfo {\n      ...BaseCategoryFragment\n      __typename\n    }\n    parentCategoryInfoList {\n      ...BaseCategoryFragment\n      __typename\n    }\n    baseFacetCategoryList {\n      ...FacetCategoryFragment\n      __typename\n    }\n    brandList {\n      id\n      name\n      count\n      __typename\n    }\n    appliedFilter {\n      brandList {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    seoMeta {\n      title\n      description\n      keywords\n      paginationPrev\n      paginationNext\n      canonical\n      robots\n      __typename\n    }\n    seoOverwritePath\n    dataLayer {\n      page_info {\n        marketplace\n        device\n        ctrl\n        project\n        page_products {\n          brand\n          currency\n          item_id\n          prod_id\n          prod_image_url\n          prod_name\n          prod_uid\n          prod_url\n          stock_available\n          __typename\n        }\n        page_cat {\n          cat_id\n          cat_name\n          cat_mpath\n          __typename\n        }\n        __typename\n      }\n      search_info {\n        search_keyword\n        raw_search_keyword\n        search_type\n        filters {\n          filter_active\n          filter_name\n          filter_value\n          filter_list {\n            filter_checked\n            filter_label\n            filter_qty\n            __typename\n          }\n          __typename\n        }\n        campaigns {\n          campaign_active\n          campaign_name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SearchResultItemFragment on SearchResultItem {\n  baseSku\n  itemId\n  itemName\n  itemUrl\n  itemPrice {\n    min\n    max\n    __typename\n  }\n  itemListPrice {\n    min\n    max\n    __typename\n  }\n  itemOriginalPrice {\n    min\n    max\n    __typename\n  }\n  itemStatus\n  itemImageUrl\n  shopId\n  shopUrl\n  shopPath\n  shopName\n  review {\n    reviewScore\n    reviewCount\n    reviewUrl\n    __typename\n  }\n  point {\n    min\n    max\n    magnification\n    __typename\n  }\n  campaignType\n  isAdultProduct\n  hideDiscountInfo\n  __typename\n}\n\nfragment BaseCategoryFragment on SearchPageCategoryType {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  __typename\n}\n\nfragment FacetCategoryFragment on SearchPageFacetCategory {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  count\n  __typename\n}\n"}

    def callback(self, ch, method, properties, body):
        cur_date = datetime.now().date()
        parameters = json.loads(body)
        self.search_page_payload['variables']['parameters'] = parameters
        html = self.downloader(self.search_page_url, json_data=self.search_page_payload)
        api_data = json.loads(html)
        products = api_data['data']['searchPage']['result']['items']
        additional_products_data = api_data['data']['searchPage']['dataLayer']['page_info']['page_products']
        products_with_new_fields = []
        for product, additional_data in zip(products, additional_products_data):
            product['currency'] = additional_data['currency']
            product['stock_available'] = additional_data['stock_available']
            products_with_new_fields.append(product)
        products = products_with_new_fields
        requests.get(self.fluentd_s3_url, json=products)
        products_data = []
        for product in products:
            products_data.append({
                'date': cur_date.strftime('%Y-%m-%d'),
                'currency': product['currency'],
                'price_min': product['itemPrice']['min'],
                'price_max': product['itemPrice']['max'],
                'stock_available': product['stock_available'],
                'name': product['itemName'],
                'shop_id': product['shopId'],
                'shop_name': product['shopName']
            })
        requests.get(self.fluentd_postgres_product_url, json=products_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.ch.basic_qos(prefetch_count=1)
        self.ch.basic_consume(
            queue='rakuten_products', on_message_callback=self.callback)
        self.ch.start_consuming()

if __name__ == '__main__':
    rate_limiter = RateLimiter('rakuten_crawler')
    redis_cache = RedisCache()
    downloader = Downloader(rate_limiter, cache=redis_cache, method='post')
    try:
        rakuten_product_worker = RakutenProductWorker(downloader)
        rakuten_product_worker.run()
    except:
        rakuten_product_worker.connection = None
    finally:
        if rakuten_product_worker.connection is not None:
            rakuten_product_worker.connection.close()
