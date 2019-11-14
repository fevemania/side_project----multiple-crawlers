import requests
import json
import time
import pymysql
from pprint import pprint
import pika


conn = pymysql.connect(host='localhost', user='root', passwd='mypass', db='mysql', charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
cur.execute('USE db')
headers = {'User-Agent': 'Googlebot',}

def send_urls():
    cur.execute('SELECT category_id, category_name FROM categories')
    #result = cur.fetchall()
    result = cur.fetchall()
    credentials = pika.PlainCredentials('admin', 'mypass')
    connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='categories', durable=True)
    for row in result:
        channel.basic_publish(
            exchange='', 
            routing_key='categories', 
            body=json.dumps(row),
            properties=pika.BasicProperties(
                delivery_mode=2,  
            ))
    connection.close()

if __name__ == '__main__':
    try:
        send_urls()
    finally:
        cur.close()
        conn.close()
