import requests
import json
import time
import pymysql
from pprint import pprint

conn = pymysql.connect(host='localhost', user='root', passwd='mypass', db='mysql', charset='utf8mb4')
cur = conn.cursor()
cur.execute('USE db')
headers = {'User-Agent': 'Googlebot',}

def shopee_scraper(keyword, n_items):
    url1 = f'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={keyword}&limit={n_items}'
    r = requests.get(url1, headers=headers)
    api1_data = json.loads(r.text)
    
    for i in range(n_items): 
         itemid = api1_data['items'][i]['itemid']
         shopid = api1_data['items'][i]['shopid']

         url2 = f'https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}'
         r = requests.get(url2, headers=headers)
         api2_data = json.loads(r.text)
         time.sleep(0.2)

def get_categories():
    cur.execute('SELECT * FROM categories')
    result = cur.fetchall()
    if result:
        return result
    else:
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

def shopee_crawler(categories):
    n_items = 50
    for category in categories:
        offset = 0
        url = f'https://shopee.tw/api/v2/search_items/?by=pop&fe_categoryids={category[0]}&limit={n_items}&newest={offset}'
        r = requests.get(url, headers=headers)
        api_data = json.loads(r.text)

        while api_data['items'] is not None:
            data_list = []
            for i in range(len(api_data['items'])):
                item = api_data['items'][i]
                itemid = item['itemid']
                shopid = item['shopid']
                url2 = f'https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}'
                api2_data = requests.get(url2, headers=headers)
                price_min = api2_data['item']['price_min']
                price_max = api2_data['item']['price_max']
                data_list.append((itemid, item['name'], price_min, price_max, category[0]))

            sql = 'INSERT INTO products (product_id, product_name, price_min, price_max, category_id) VALUES (%s, %s, %s, %s, %s)'
            cur.executemany(sql, data_list)
            conn.commit()
            offset += n_items
            print(offset)
            url = f'https://shopee.tw/api/v2/search_items/?by=pop&fe_categoryids={category[0]}&limit={n_items}&newest={offset}'
            r = requests.get(url, headers=headers)
            api_data = json.loads(r.text)
            time.sleep(0.2)
        break
    #if api_data['items'] is not None:
    #    print(len(api_data['items']))
def tt():
    sql = 'SELECT * FROM products'
    cur.execute(sql)
    result = cur.fetchall()
    print(result[0])
    
if __name__ == '__main__':
    try:
    #    while len(links) > 0:
        #categories = get_categories()
        #shopee_crawler(categories)
        tt()
    #    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    #    links = getLinks(newArticle)
    finally:
        cur.close()
        conn.close()
