FROM python

COPY side_project/wait-for-it.sh wait-for-it.sh
COPY side_project/restful_api/requirements.txt requirements.txt
COPY side_project/restful_api/flask_run.sh flask_run.sh
COPY side_project/restful_api/app.py app.py
COPY side_project/restful_api/config.py config.py
COPY side_project/restful_api/http_status.py http_status.py
COPY side_project/restful_api/models.py models.py
COPY side_project/restful_api/views.py views.py

RUN pip install -r requirements.txt
RUN chmod +x flask_run.sh
