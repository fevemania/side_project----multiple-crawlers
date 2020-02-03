import os 
import pika
import sys
from datetime import datetime
import requests
import json
from time import time
import socket
import redis
import pdb
from datetime import timedelta
import psycopg2
import math

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')

class RakutenCrawlerRoutine:
    def __init__(self, fluentd_port=9880):
        self.search_page_url = 'https://www.rakuten.com.tw/graphql'
        self.conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
        self.cursor = self.conn.cursor()
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rakuten_categories', durable=True)

    def run(self):
        cur_date = datetime.now().date()
        tablename = 'product_{}'.format(cur_date)
        self.cursor.execute("SELECT to_regclass('public.{}')".format(tablename))
        result = self.cursor.fetchone()
        if result[0] is None:
            self.cursor.execute("CREATE TABLE \"{}\" PARTITION OF product FOR VALUES FROM ('{}') TO ('{}')".format(
                tablename, cur_date, cur_date + timedelta(days=1)))
            self.conn.commit()

        self.cursor.execute("select id, level, is_leaf_node, page_count, name from category")
        categories = self.cursor.fetchall()
        if categories:
            for category in categories:
                row = (category[0], category[1], category[2], category[3], category[4], True)
                self.channel.basic_publish(
                    exchange='',
                    routing_key='rakuten_categories',
                    body=json.dumps(row),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))
        else:
            parameters = {}
            search_page_payload = {
                    "operationName":"fetchSearchPageResults",
                    "variables":{"parameters":parameters},
                    "query":"query fetchSearchPageResults($parameters: SearchInputType!) {\n  searchPage(parameters: $parameters) {\n    serializedKey\n    title\n    result {\n      abTestVariation\n      items {\n        ...SearchResultItemFragment\n        __typename\n      }\n      totalItems\n      conjunction\n      __typename\n    }\n    recommendationRefItem {\n      shopId\n      itemId\n      rakutenCategoryTree\n      __typename\n    }\n    pagination {\n      itemsPerPage\n      pageNumber\n      totalItems\n      __typename\n    }\n    currentCategoryInfo {\n      ...BaseCategoryFragment\n      __typename\n    }\n    parentCategoryInfoList {\n      ...BaseCategoryFragment\n      __typename\n    }\n    baseFacetCategoryList {\n      ...FacetCategoryFragment\n      __typename\n    }\n    brandList {\n      id\n      name\n      count\n      __typename\n    }\n    appliedFilter {\n      brandList {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    seoMeta {\n      title\n      description\n      keywords\n      paginationPrev\n      paginationNext\n      canonical\n      robots\n      __typename\n    }\n    seoOverwritePath\n    dataLayer {\n      page_info {\n        marketplace\n        device\n        ctrl\n        project\n        page_products {\n          brand\n          currency\n          item_id\n          prod_id\n          prod_image_url\n          prod_name\n          prod_uid\n          prod_url\n          stock_available\n          __typename\n        }\n        page_cat {\n          cat_id\n          cat_name\n          cat_mpath\n          __typename\n        }\n        __typename\n      }\n      search_info {\n        search_keyword\n        raw_search_keyword\n        search_type\n        filters {\n          filter_active\n          filter_name\n          filter_value\n          filter_list {\n            filter_checked\n            filter_label\n            filter_qty\n            __typename\n          }\n          __typename\n        }\n        campaigns {\n          campaign_active\n          campaign_name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SearchResultItemFragment on SearchResultItem {\n  baseSku\n  itemId\n  itemName\n  itemUrl\n  itemPrice {\n    min\n    max\n    __typename\n  }\n  itemListPrice {\n    min\n    max\n    __typename\n  }\n  itemOriginalPrice {\n    min\n    max\n    __typename\n  }\n  itemStatus\n  itemImageUrl\n  shopId\n  shopUrl\n  shopPath\n  shopName\n  review {\n    reviewScore\n    reviewCount\n    reviewUrl\n    __typename\n  }\n  point {\n    min\n    max\n    magnification\n    __typename\n  }\n  campaignType\n  isAdultProduct\n  hideDiscountInfo\n  __typename\n}\n\nfragment BaseCategoryFragment on SearchPageCategoryType {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  __typename\n}\n\nfragment FacetCategoryFragment on SearchPageFacetCategory {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  count\n  __typename\n}\n"}

            # search all basic category
            resp = requests.post(self.search_page_url, json=search_page_payload)
            api_data = json.loads(resp.text)
            categories = api_data['data']['searchPage']['baseFacetCategoryList']
            for category in categories:
                row = (category['id'], category['level'], category['isLeafNode'], int(math.ceil(category['count']/20)), category['name'], False)
                self.channel.basic_publish(
                    exchange='',
                    routing_key='rakuten_categories',
                    body=json.dumps(row),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))

if __name__ == '__main__':
    try:
        rakuten_crawler_routine = RakutenCrawlerRoutine()
        rakuten_crawler_routine.run()
    except:
        print('here')
        rakuten_crawler_routine.cursor.close()
        rakuten_crawler_routine.conn.close()
        rakuten_crawler_routine.connection.close()

