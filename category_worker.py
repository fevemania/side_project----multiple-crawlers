#!/usr/bin/env python
import pika
import sys
import time

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    try:
        credentials = pika.PlainCredentials('admin', 'mypass')
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', credentials=credentials))
        channel = connection.channel()
        
        channel.queue_declare(queue='categories', durable=True)
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
                queue='categories', on_message_callback=callback)
        channel.start_consuming()
    except:
        sys.exit(2)
