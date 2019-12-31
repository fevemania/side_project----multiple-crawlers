FROM python
<<<<<<< HEAD
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
COPY shopee_crawler/requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD shopee_crawler/crawler_routine/code /mnt
ADD shopee_crawler/crawler_routine/job /etc/cron.d/job
RUN chmod 0644 /etc/cron.d/job
WORKDIR /mnt
RUN chmod 0644 crontab.sh

RUN touch /var/log/cron.log
RUN apt-get update && apt-get -y install cron
=======

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/shopee_crawler/common/requirements.txt requirements.txt
COPY side_project/shopee_crawler/crawler_routine/code /mnt
COPY side_project/shopee_crawler/crawler_routine/job /etc/cron.d/job

RUN chmod +x ./wait-for-it.sh
RUN pip install -r requirements.txt
RUN chmod 0644 /etc/cron.d/job
RUN chmod 0644 /mnt/crontab.sh
RUN touch /var/log/cron.log
RUN apt-get update && apt-get -y install cron

>>>>>>> dev_devops_test
CMD cron && tail -f /var/log/cron.log
