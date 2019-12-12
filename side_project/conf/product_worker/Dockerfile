FROM python
RUN pip install pika requests redis
COPY product_worker.py product_worker.py
COPY downloader.py downloader.py
COPY rate_limiter.py rate_limiter.py
COPY redis_cache.py redis_cache.py
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
