FROM python

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/crawler/common /common
COPY side_project/crawler/shopee/crawler_routine/code /mnt
COPY side_project/crawler/shopee/crawler_routine/job /etc/cron.d/job

RUN chmod +x ./wait-for-it.sh
RUN pip install -r /common/requirements.txt
RUN chmod 0644 /etc/cron.d/job
RUN chmod 0644 /mnt/crontab.sh
RUN touch /var/log/cron.log
RUN apt-get update && apt-get -y install vim cron

CMD cron && tail -f /var/log/cron.log
