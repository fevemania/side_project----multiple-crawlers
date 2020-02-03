FROM python

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/crawler/common /common
COPY side_project/crawler/shopee/category_crawler/category_crawler.py category_crawler.py

RUN chmod +x ./wait-for-it.sh
RUN pip install -r /common/requirements.txt
