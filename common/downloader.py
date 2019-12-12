import requests
import pdb
import time

class Downloader:
    def __init__(self, rate_limiter, user_agent='Googlebot', proxies=None, cache={}, timeout=60):
        self.rate_limiter = rate_limiter
        self.headers = {'User-Agent': user_agent}
        self.proxies = proxies
        self.cache = cache
        self.num_retries = None
        self.timeout = timeout

    def __call__(self, url, num_retries=2):
        self.num_retries = num_retries
        try:
            result = self.cache[url]
        except KeyError:
            result = None
        except Exception as ex: #KeyError
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        #if result and self.num_retries and 500 <= result['code'] < 600:
        #    result = None
        if result is None:
            self.rate_limiter.wait()
            result = self.download(url, self.headers, self.proxies) # to-do: proxies
            self.cache[url] = result
        return result['html']


    def download(self, url, headers, proxies):
        try:
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=self.timeout)
            html = resp.text
            if resp.status_code >= 400:
                print('Download error:', resp.status_code)
                html = None
                if self.num_retries and 500 <= resp.status_code < 600:
                    self.num_retries -= 1
                    return self.download(url, headers, proxies)
        except requests.exceptions.RequestException as e:
            print('Download error:', e)
            print('wait')
            time.sleep(30)
            return {'html': None, 'code': 500}
        return {'html': html, 'code': resp.status_code}
