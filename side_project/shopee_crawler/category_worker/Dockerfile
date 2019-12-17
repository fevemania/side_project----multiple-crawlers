FROM python
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
COPY shopee_crawler/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY shopee_crawler/downloader.py downloader.py
COPY shopee_crawler/rate_limiter.py rate_limiter.py
COPY shopee_crawler/redis_cache.py redis_cache.py
COPY shopee_crawler/category_worker.py category_worker.py
