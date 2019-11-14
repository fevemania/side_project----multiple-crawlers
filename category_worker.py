#!/usr/bin/env python
import pika
import sys
import time
import socket
import os
import json
import requests

n_items=100
offset = 0
headers = {'User-Agent': 'Googlebot',}
url_pattern = 'https://shopee.tw/api/v2/search_items/?by=pop&fe_categoryids={}&limit={}&newest={}'

def callback(ch, method, properties, body):
    global offset
    row = json.loads(body)
    r = requests.get(url_pattern.format(row['category_id'], n_items, offset), headers=headers)
    api_data = json.loads(r.text)
    product = {}
    try:
        while api_data['items'] is not None:
            for i in range(len(api_data['items'])):
                item = api_data['items'][i]
                product['itemid'] = item['itemid']
                product['shopid'] = item['shopid']
                product['name'] = item['name']
                ch2.basic_publish(
                    exchange='',
                    routing_key='products',
                    body=json.dumps(product),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))
            offset += n_items
            r = requests.get(url_pattern.format(row['category_id'], n_items, offset), headers=headers) 
            api_data = json.loads(r.text)
    except:
        connection.close()
            

        
    ch.basic_ack(delivery_tag=method.delivery_tag)

#def is_open(ip, port):
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    try:
#        s.connect((ip, int(port)))
#        s.shutdown(2)
#        print('True')
#    except:
#        print('False')

if __name__ == '__main__':
#   is_open(os.environ.get('RABBIT_HOST'), 5672)
    try:
        global ch2 
        global connection
        credentials = pika.PlainCredentials('admin', 'mypass')
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'), credentials=credentials))
        ch1 = connection.channel()
        ch2 = connection.channel()
        ch1.queue_declare(queue='categories', durable=True)
        ch2.queue_declare(queue='products', durable=True)
        ch1.basic_qos(prefetch_count=1)
        ch1.basic_consume(
                queue='categories', on_message_callback=callback)
        ch1.start_consuming()
    except:
        sys.exit(2)
    finally:
        connection.close()
