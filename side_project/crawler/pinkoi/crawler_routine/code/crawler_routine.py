import os 
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

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')

class PinkoiCrawlerRoutine:
    def __init__(self):
        address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
        self.product_url = 'https://www.pinkoi.com/apiv2/browse?category={}&page={}'
        self.conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
        self.cursor = self.conn.cursor()
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='pinkoi_products', durable=True)        

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
                    url = self.product_url.format(category_id, page_id)
                    self.channel.basic_publish(
                        exchange='',
                        routing_key='pinkoi_products',
                        body=json.dumps(url),
                        properties=pika.BasicProperties(
                            delivery_mode=2,
                        ))

if __name__ == '__main__':
    try:
        pinkoi_crawler_routine = PinkoiCrawlerRoutine()
        pinkoi_crawler_routine.run()
    except:
        print('here')
        pinkoi_crawler_routine.cursor.close()
        pinkoi_crawler_routine.conn.close()
        pinkoi_crawler_routine.connection.close()

