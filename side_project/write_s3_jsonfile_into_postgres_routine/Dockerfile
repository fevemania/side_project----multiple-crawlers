FROM python
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
COPY write_s3_jsonfile_into_postgres_routine/requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD write_s3_jsonfile_into_postgres_routine/code /mnt
ADD write_s3_jsonfile_into_postgres_routine/job /etc/cron.d/job
RUN chmod 0644 /etc/cron.d/job
WORKDIR /mnt
RUN chmod 0644 crontab.sh

RUN touch /var/log/cron.log
RUN apt-get update && apt-get -y install cron
CMD cron && tail -f /var/log/cron.log
