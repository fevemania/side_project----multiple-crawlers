FROM python

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/crawler/common /common
COPY side_project/crawler/rakuten/category_worker/category_worker.py category_worker.py

RUN chmod +x ./wait-for-it.sh
RUN pip install -r /common/requirements.txt
