FROM python
RUN apt-get update && apt-get -y install cron
COPY write_s3_jsonfile_into_postgres_routine/requirements.txt requirements.txt
RUN pip install -r requirements.txt 
COPY wait-for-it.sh wait-for-it.sh
COPY write_s3_jsonfile_into_postgres_routine/cronjobs /etc/cron.d/cronjobs
COPY write_s3_jsonfile_into_postgres_routine/write_s3_jsonfile_into_postgres.py write_s3_jsonfile_into_postgres.py
RUN chmod 0644 /etc/cron.d/cronjobs && crontab /etc/cron.d/cronjobs
