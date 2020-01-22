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

class PinkoiProductCrawler:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.product_url = 'https://www.pinkoi.com/apiv2/browse?category={}&page={}'
        self.fluentd_url1 = 'http://{}:{}/s3.http.access'.format(address, fluentd_port)
        self.fluentd_url2 = 'http://{}:{}/postgres.access'.format(address, fluentd_port)

    def run(self):
        cur_date = datetime.now().date()
        for category_id in range(16):
            if category_id != 7:
                for page_id in range(1, 501):
                    html = self.downloader(self.product_url.format(category_id, page_id))
                    try:
                        if html is not None:
                            api_data = json.loads(html)
                            product_list = api_data['result'][0]['hits']['hits']
                            if product_list:
                                #requests.get(self.fluentd_url, json=product_list)
                                product_data = []
                                for product in product_list:
                                    product_data.append({
                                        'date': cur_date,
                                        'currency': product['fields']['currency']['name'],
                                        'price': product['fields']['price'],
                                        'name': product['fields']['title']
                                    })
                                requests.get(self.fluentd_url2, json=product_data)
                        else:
                            print('Oh no')
                            print('product html is None')
                    except Exception as e:
                        print(e.reason)

        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    rate_limiter = RateLimiter('pinkoi_crawler')
    redis_cache = RedisCache()
    downloader = Downloader(rate_limiter, cache=redis_cache)
    pinkoi_product_crawler = PinkoiProductCrawler(downloader)
    pinkoi_product_crawler.run()

