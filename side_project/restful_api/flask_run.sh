#!/bin/bash
python config_parser.py
alembic init migrations
cp alembic_env.py migrations/env.py
alembic revision --autogenerate
alembic upgrade head
#alembic db migrate
#alembic db upgrade
export FLASK_ENV=development
flask run --host="0.0.0.0"
