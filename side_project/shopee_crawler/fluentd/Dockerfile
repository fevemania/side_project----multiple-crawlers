FROM fluent/fluentd:v1.6-debian-1
USER root
RUN ["gem", "install", "fluent-plugin-s3",  "-v", "1.0.0",  "--no-document"]
RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN fluent-gem install fluent-plugin-sql 
RUN fluent-gem install pg 
#RUN ["gem", "install", "fluent-plugin-elasticsearch",  "--no-document", "--version", "3.5.2"]
COPY side_project/shopee_crawler/fluentd/fluent.conf /fluentd/etc/
USER fluent
