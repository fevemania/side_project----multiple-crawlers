import requests
import json
import time
import pymysql
from pprint import pprint

conn = pymysql.connect(host='mysql', user='admin', passwd='mypass', db='mysql', charset='utf8mb4')
cur = conn.cursor()
cur.execute('USE db')
headers = {'User-Agent': 'Googlebot',}

def crawl_categories():
    url = 'https://shopee.tw/api/v2/fe_category/get_list'
    r = requests.get(url, headers=headers)
    api_data = json.loads(r.text)
    categories = api_data['data']['category_list']
    categories = [(category['catid'], category['display_name']) for category in categories]
    #string = ','.join([str(category) for category in categories])
    #cur.executemany('INSERT INTO categories (id, name) VALUES ' + string)
    sql = 'INSERT INTO categories (category_id, category_name) VALUES (%s, %s)' 
    cur.executemany(sql, categories)
    conn.commit()
    return categories

if __name__ == '__main__':
    try:
        crawl_categories()
    finally:
        cur.close()
        conn.close()
