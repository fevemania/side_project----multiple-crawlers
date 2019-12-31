FROM python
<<<<<<< HEAD
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
COPY shopee_crawler/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY shopee_crawler/category_crawler.py category_crawler.py
=======

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/shopee_crawler/common/requirements.txt requirements.txt
COPY side_project/shopee_crawler/category_crawler/category_crawler.py category_crawler.py

RUN chmod +x ./wait-for-it.sh
RUN pip install -r requirements.txt
>>>>>>> dev_devops_test
