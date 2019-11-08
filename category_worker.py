#!/usr/bin/env python
import pika
import sys
import time
import socket
import os

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
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
        credentials = pika.PlainCredentials('admin', 'mypass')
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('RABBIT_HOST', 'localhost'), credentials=credentials))
        channel = connection.channel()
        
        channel.queue_declare(queue='categories', durable=True)
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
                queue='categories', on_message_callback=callback)
        channel.start_consuming()
    except:
        sys.exit(2)
