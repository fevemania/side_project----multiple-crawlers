import requests
import json
import time
import psycopg2
import pika
import os
import socket
from datetime import datetime

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')

conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
cur = conn.cursor()
headers = {'User-Agent': 'Googlebot',}

def send_categories():
    cur.execute('SELECT category_id, category_name FROM categories')
    result = cur.fetchall()
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='categories', durable=True)
    print("send")
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
