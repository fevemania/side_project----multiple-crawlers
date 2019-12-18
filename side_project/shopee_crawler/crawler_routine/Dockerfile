FROM python

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/shopee_crawler/common/requirements.txt requirements.txt
COPY side_project/shopee_crawler/crawler_routine/crontab /mnt
COPY side_project/shopee_crawler/crawler_routine/job /etc/cron.d/job

RUN chmod +x ./wait-for-it.sh
RUN pip install -r requirements.txt
RUN chmod 0644 /etc/cron.d/job
RUN chmod 0644 /mnt/crontab.sh
RUN touch /var/log/cron.log
RUN apt-get update && apt-get -y install cron

CMD cron && tail -f /var/log/cron.log
