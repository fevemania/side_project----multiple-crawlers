import os 
import sys
from datetime import datetime
import requests
import json
from time import time
import socket
import redis
sys.path.append('/')
from common.downloader import Downloader
from common.rate_limiter import RateLimiter
from common.redis_cache import RedisCache
import pdb
from datetime import timedelta
import psycopg2

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))

class PinkoiProductCrawler:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.product_url = 'https://www.pinkoi.com/apiv2/browse?category={}&page={}'
        self.fluentd_to_s3_url = 'http://{}:{}/s3.http.access'.format(address, fluentd_port)
        self.fluentd_to_postgres_url = 'http://{}:{}/postgres.access'.format(address, fluentd_port)
        self.conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
        self.cursor = self.conn.cursor()

    def run(self):
        cur_date = datetime.now().date()
        tablename = 'product_{}'.format(cur_date)
        self.cursor.execute("SELECT to_regclass('public.{}')".format(tablename))
        result = self.cursor.fetchone()
        if result[0] is None:
            self.cursor.execute("CREATE TABLE \"{}\" PARTITION OF product FOR VALUES FROM ('{}') TO ('{}')".format(
                tablename, cur_date, cur_date + timedelta(days=1)))
            self.conn.commit()

        for category_id in range(16):
            if category_id != 7:
                for page_id in range(1, 501):
                    html = self.downloader(self.product_url.format(category_id, page_id))
                    try:
                        if html is not None:
                            api_data = json.loads(html)
                            product_list = api_data['result'][0]['hits']['hits']
                            if product_list:
                                requests.get(self.fluentd_to_s3_url, json=product_list)
                                product_data = []
                                for product in product_list:
                                    product_data.append({
                                        'date': cur_date.strftime('%Y-%m-%d'),
                                        'currency': product['fields']['currency']['name'],
                                        'price': product['fields']['price'],
                                        'name': product['fields']['title']
                                    })
                                requests.get(self.fluentd_to_postgres_url, json=product_data)
                        else:
                            print('Oh no')
                            print('product html is None')
                    except Exception as e:
                        print(e.reason)

if __name__ == '__main__':
    rate_limiter = RateLimiter('pinkoi_crawler')
    redis_cache = RedisCache()
    downloader = Downloader(rate_limiter, cache=redis_cache)
    try:
        pinkoi_product_crawler = PinkoiProductCrawler(downloader)
        pinkoi_product_crawler.run()
    except:
        print('here')
        pinkoi_product_crawler.cursor.close()
        pinkoi_product_crawler.conn.close()

