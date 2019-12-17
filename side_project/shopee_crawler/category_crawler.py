import requests
import json
import time
import psycopg2
import socket
import os

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))

conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
#conn = psycopg2.connect(database='db', user='admin', password='mypass', host='localhost', port='5432')
cur = conn.cursor()
headers = {'User-Agent': 'Googlebot',}

def crawl_categories():
    sql = "SELECT * FROM categories"
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        print('categories information already store.')
    else:
        url = 'https://shopee.tw/api/v2/fe_category/get_list'
        r = requests.get(url, headers=headers)
        api_data = json.loads(r.text)
        categories = api_data['data']['category_list']
        categories = [(category['catid'], category['display_name']) for category in categories]
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
