FROM python
<<<<<<< HEAD
COPY restful_api/requirements.txt requirements.txt
COPY wait-for-it.sh wait-for-it.sh
RUN pip install -r requirements.txt
COPY restful_api/flask_run.sh flask_run.sh
RUN chmod +x flask_run.sh
COPY restful_api/app.py app.py
COPY restful_api/config.py config.py
COPY restful_api/http_status.py http_status.py
COPY restful_api/models.py models.py
COPY restful_api/views.py views.py
=======

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
>>>>>>> dev_devops_test
