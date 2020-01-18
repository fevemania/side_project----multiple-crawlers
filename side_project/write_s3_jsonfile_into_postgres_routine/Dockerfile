FROM python

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/write_s3_jsonfile_into_postgres_routine/requirements.txt requirements.txt
RUN apt-get update && apt-get install -y vim
RUN chmod +x ./wait-for-it.sh
RUN pip install -r requirements.txt
COPY side_project/write_s3_jsonfile_into_postgres_routine/code /mnt
COPY side_project/write_s3_jsonfile_into_postgres_routine/job /etc/cron.d/job

RUN chmod 0644 /etc/cron.d/job
RUN chmod 0644 /mnt/crontab.sh
RUN touch /var/log/cron.log
RUN apt-get update && apt-get -y install cron

CMD cron && tail -f /var/log/cron.log
