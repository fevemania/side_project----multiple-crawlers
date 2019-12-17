FROM python
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
COPY shopee_crawler/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY shopee_crawler/category_crawler.py category_crawler.py
