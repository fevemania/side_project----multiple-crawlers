import requests
import json
import time
import pymysql
from pprint import pprint
import pika


conn = pymysql.connect(host='mysql', user='admin', passwd='mypass', db='db', charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
cur.execute('USE db')
headers = {'User-Agent': 'Googlebot',}

def send_categories():
    cur.execute('SELECT category_id, category_name FROM categories')
    result = cur.fetchall()
    credentials = pika.PlainCredentials('admin', 'mypass')
    connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
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
        send_categories()
    finally:
        cur.close()
        conn.close()
