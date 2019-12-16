FROM python
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
