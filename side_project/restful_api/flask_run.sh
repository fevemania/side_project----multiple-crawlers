#!/bin/bash
python config_parser.py
alembic init pinkoi/migrations
#cp shopee/alembic_env.py shopee/migrations/env.py
#cp carousell/alembic_env.py carousell/migrations/env.py
cp /pinkoi/alembic_env.py /pinkoi/migrations/env.py
alembic -n pinkoi_schema revision --autogenerate
alembic -n pinkoi_schema upgrade head
#alembic db migrate
#alembic db upgrade
export FLASK_ENV=development
flask run --host="0.0.0.0"
