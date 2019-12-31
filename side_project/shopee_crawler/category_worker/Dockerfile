FROM python
<<<<<<< HEAD
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
COPY shopee_crawler/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY shopee_crawler/downloader.py downloader.py
COPY shopee_crawler/rate_limiter.py rate_limiter.py
COPY shopee_crawler/redis_cache.py redis_cache.py
COPY shopee_crawler/category_worker.py category_worker.py
=======

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/shopee_crawler/common/requirements.txt requirements.txt
COPY side_project/shopee_crawler/common/downloader.py downloader.py
COPY side_project/shopee_crawler/common/rate_limiter.py rate_limiter.py
COPY side_project/shopee_crawler/common/redis_cache.py redis_cache.py
COPY side_project/shopee_crawler/category_worker/category_worker.py category_worker.py

RUN chmod +x ./wait-for-it.sh
RUN pip install -r requirements.txt
>>>>>>> dev_devops_test
