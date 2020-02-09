import os
import socket
import requests
address = socket.gethostbyname(os.environ.get('FLUENTD_HOST', 'localhost'))
elasticsearch_url = 'http://{}:{}/elasticsearch'.format(address, 9880)
obj = {
  "name": "John Doe"
}
print(requests.put(elasticsearch_url, json=obj))
#print(requests.get(elasticsearch_url+'/customer/_doc/1', json={}).text)
#print(requests.get(elasticsearch_url+'/_cat/indices', json={}).text)

