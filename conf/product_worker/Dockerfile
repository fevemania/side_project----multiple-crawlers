FROM python
RUN pip install pika requests redis
COPY conf/product_worker/product_worker.py product_worker.py
COPY common/downloader.py downloader.py
COPY common/rate_limiter.py rate_limiter.py
COPY common/redis_cache.py redis_cache.py
COPY common/wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
