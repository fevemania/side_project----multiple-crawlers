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

class RakutenProductCrawler:
    def __init__(self, downloader, fluentd_port=9880):
        self.downloader = downloader
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.product_url = 'https://www.rakuten.com.tw/graphql'
        #self.fluentd_to_s3_url = 'http://{}:{}/s3.http.access'.format(address, fluentd_port)
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

        #html = self.downloader(self.product_url)
        parameters = {}
        payload = {"operationName":"fetchSearchPageResults","variables":{"parameters":parameters,"query":"query fetchSearchPageResults($parameters: SearchInputType!) {\n  searchPage(parameters: $parameters) {\n    serializedKey\n    title\n    result {\n      abTestVariation\n      items {\n        ...SearchResultItemFragment\n        __typename\n      }\n      totalItems\n      conjunction\n      __typename\n    }\n    recommendationRefItem {\n      shopId\n      itemId\n      rakutenCategoryTree\n      __typename\n    }\n    pagination {\n      itemsPerPage\n      pageNumber\n      totalItems\n      __typename\n    }\n    currentCategoryInfo {\n      ...BaseCategoryFragment\n      __typename\n    }\n    parentCategoryInfoList {\n      ...BaseCategoryFragment\n      __typename\n    }\n    baseFacetCategoryList {\n      ...FacetCategoryFragment\n      __typename\n    }\n    brandList {\n      id\n      name\n      count\n      __typename\n    }\n    appliedFilter {\n      brandList {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    seoMeta {\n      title\n      description\n      keywords\n      paginationPrev\n      paginationNext\n      canonical\n      robots\n      __typename\n    }\n    seoOverwritePath\n    dataLayer {\n      page_info {\n        marketplace\n        device\n        ctrl\n        project\n        page_products {\n          brand\n          currency\n          item_id\n          prod_id\n          prod_image_url\n          prod_name\n          prod_uid\n          prod_url\n          stock_available\n          __typename\n        }\n        page_cat {\n          cat_id\n          cat_name\n          cat_mpath\n          __typename\n        }\n        __typename\n      }\n      search_info {\n        search_keyword\n        raw_search_keyword\n        search_type\n        filters {\n          filter_active\n          filter_name\n          filter_value\n          filter_list {\n            filter_checked\n            filter_label\n            filter_qty\n            __typename\n          }\n          __typename\n        }\n        campaigns {\n          campaign_active\n          campaign_name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SearchResultItemFragment on SearchResultItem {\n  baseSku\n  itemId\n  itemName\n  itemUrl\n  itemPrice {\n    min\n    max\n    __typename\n  }\n  itemListPrice {\n    min\n    max\n    __typename\n  }\n  itemOriginalPrice {\n    min\n    max\n    __typename\n  }\n  itemStatus\n  itemImageUrl\n  shopId\n  shopUrl\n  shopPath\n  shopName\n  review {\n    reviewScore\n    reviewCount\n    reviewUrl\n    __typename\n  }\n  point {\n    min\n    max\n    magnification\n    __typename\n  }\n  campaignType\n  isAdultProduct\n  hideDiscountInfo\n  __typename\n}\n\nfragment BaseCategoryFragment on SearchPageCategoryType {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  __typename\n}\n\nfragment FacetCategoryFragment on SearchPageFacetCategory {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  count\n  __typename\n}\n"}
        # search all basic category 
        html = requests.post(self.product_url, json=payload)
        api_data = json.loads(html.text)
        basic_categories = api_data['data']['searchPage']['baseFacetCategoryList']
        for basic_category in basic_categories:
            basic_category['id']
        
        

        
        parameters = {"pageNumber":2,"categoryId":"6879"}
        html = requests.post(self.product_url, json=payload)
        api_data = json.loads(html.text)
        products = api_data['data']['searchPage']['result']['items']
        for product in products:
            print(product['prod_name'])

                  # try:
                  #     if html is not None:
                  #         api_data = json.loads(html)
                  #         product_list = api_data['result'][0]['hits']['hits']
                  #         if product_list:
                  #            #requests.get(self.fluentd_to_s3_url, json=product_list)
                  #             product_data = []
                  #             for product in product_list:
                  #                 product_data.append({
                  #                     'date': cur_date.strftime('%Y-%m-%d'),
                  #                     'currency': product['fields']['currency']['name'],
                  #                     'price': product['fields']['price'],
                  #                     'name': product['fields']['title']
                  #                 })
                  #             requests.get(self.fluentd_to_postgres_url, json=product_data)
                  #     else:
                  #         print('Oh no')
                  #         print('product html is None')
                  # except Exception as e:
                  #     print(e.reason)


if __name__ == '__main__':
    rate_limiter = RateLimiter('rakuten_crawler')
    redis_cache = RedisCache()
    downloader = Downloader(rate_limiter, cache=redis_cache)
    try:
        rakuten_product_crawler = RakutenProductCrawler(downloader)
        rakuten_product_crawler.run()
    except:
        print('here')
        rakuten_product_crawler.cursor.close()
        rakuten_product_crawler.conn.close()

