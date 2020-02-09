FROM python

RUN apt-get update && apt-get install -y vim

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/crawler/common /common
COPY side_project/crawler/shopee/product_worker/product_worker.py product_worker.py

RUN chmod +x ./wait-for-it.sh
RUN pip install -r /common/requirements.txt
