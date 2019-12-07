FROM mysql:5.7
ENV MYSQL_DATABASE db
ENV MYSQL_USER admin
ENV MYSQL_PASSWORD mypass
ENV MYSQL_ROOT_PASSWORD mypass

COPY ./mysqldb/ /docker-entrypoint-initdb.d/

