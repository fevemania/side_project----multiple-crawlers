FROM python

RUN apt-get update && apt-get install -y vim
COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/restful_api/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY side_project/restful_api/flask_run.sh flask_run.sh
RUN chmod +x flask_run.sh

COPY side_project/restful_api/alembic.ini alembic.ini
COPY side_project/restful_api/app.py app.py
COPY side_project/restful_api/config_parser.py config_parser.py
COPY side_project/restful_api/shopee /shopee
COPY side_project/restful_api/pinkoi /pinkoi
COPY side_project/restful_api/rakuten /rakuten
COPY side_project/restful_api/common /common
#COPY side_project/restful_api/config.py config.py
#COPY side_project/restful_api/http_status.py http_status.py
#COPY side_project/restful_api/prac2.py prac2.py
#COPY side_project/restful_api/table_partition_with_date.py table_partition_with_date.py
