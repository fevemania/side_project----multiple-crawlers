import os 
import sys
import pika
import requests
import json
import time
from pprint import pprint
import socket

headers = {'User-Agent': 'Googlebot',}
url_pattern = 'https://shopee.tw/api/v2/item/get?itemid={}&shopid={}'
url_pattern2 = 'http://{}:{}/mysql.access' 
print(os.environ.get('MYSQL_HOST', 'localhost'))
fluentd_port=9880
address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))

def callback(ch, method, properties, body):
    product = json.loads(body)
    api_data = requests.get(url_pattern.format(product['itemid'], product['shopid']), headers=headers)
    product['price_min'] = api_data['item']['price_min'] / 100000
    product['price_max'] = api_data['item']['price_max'] / 100000
    requests.get(url_pattern2.format(address, fluentd_port), json=product)    
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    try:
        credentials = pika.PlainCredentials('admin', 'mypass')
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'), credentials=credentials))
        ch = connection.channel()
        ch.queue_declare(queue='products', durable=True)
        ch.basic_qos(prefetch_count=1)
        ch.basic_consume(
                queue='products', on_message_callback=callback)
        ch.start_consuming()
    except:
        sys.exit(2)
    finally:
        connection.close()
