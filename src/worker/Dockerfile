FROM python
COPY worker.py worker.py
COPY wait-for-it.sh wait-for-it.sh
RUN pip install pika requests
RUN chmod +x ./wait-for-it.sh
