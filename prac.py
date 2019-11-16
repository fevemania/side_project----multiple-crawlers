import requests
import os
import socket

url_pattern2 = 'http://{}:{}/mysql.access'
#product={'product_id': 14, 'product_name': 'good', 'price_min': 156.0, 'price_max': 156.0, 'category_id': 1}
#address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
#address = socket.gethostbyname(os.environ.get('RABBIT_HOST', 'localhost'))
address = 'localhost'
s = socket.socket()
port = 6379

#port = 5672
try:
    s.connect((address, port))
    print("Connected to %s on port %s" % (address, port))
finally:
    s.close()
#response = requests.get(url_pattern2.format(ipaddress, 9880), json=product)
#print(response.status_code, response.reason)
#print(os.environ.get('MYSQL_HOST', 'localhost'))
