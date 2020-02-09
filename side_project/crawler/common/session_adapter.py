import requests
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200)
sess.mount('https://', adapter)
