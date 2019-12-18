FROM python

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/shopee_crawler/common/requirements.txt requirements.txt
COPY side_project/shopee_crawler/category_crawler/category_crawler.py category_crawler.py

RUN chmod +x ./wait-for-it.sh
RUN pip install -r requirements.txt
