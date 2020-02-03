import requests
import sys
import time
import json

class Downloader:
    def __init__(self, rate_limiter, method, user_agent='Googlebot', proxies=None, cache={}, timeout=60):
        self.rate_limiter = rate_limiter
        self.method = method
        self.headers = {'User-Agent': user_agent}
        self.proxies = proxies
        self.cache = cache
        self.num_retries = None
        self.timeout = timeout
        self.cnt = 0

    def __call__(self, url, json_data={}, num_retries=2):
        self.num_retries = num_retries
        try:
            result = self.cache[url+json.dumps(json_data)]
        except KeyError:
            result = None
        except Exception as ex: #KeyError
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)
        if result is None or result['html'] is None:
            self.rate_limiter.wait()
            result = self.download(url, self.headers, self.proxies, json_data) # to-do: proxies
            self.cache[url] = result

        return result['html']


    def download(self, url, headers, proxies, json_data):
        while True:
            try:
                if self.method == 'get':
                    resp = requests.get(url, headers=headers, proxies=proxies, timeout=self.timeout)
                elif self.method == 'post':
                    resp = requests.post(url, json=json_data, headers=headers, proxies=proxies, timeout=self.timeout)
                else:
                    print('method should be defined either `get` or `post`')
                    sys.exit(1)
                html = resp.text
                if resp.status_code >= 400:
                    print('Download error:', resp.status_code)
                    html = None
                    if self.num_retries and 500 <= resp.status_code < 600:
                        self.num_retries -= 1
                        time.sleep(5)
                        return self.download(url, headers, proxies, json_data)
            except requests.exceptions.RequestException as e:
                print('Download error:', e)
                time.sleep(5)
                continue
            return {'html': html, 'code': resp.status_code}
