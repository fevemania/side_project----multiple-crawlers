#!/bin/bash
python config_parser.py
alembic init rakuten/migrations
#alembic init pinkoi/migrations
#cp /shopee/alembic_env.py /shopee/migrations/env.py
cp /rakuten/alembic_env.py /rakuten/migrations/env.py
#cp /pinkoi/alembic_env.py /pinkoi/migrations/env.py
alembic -n rakuten_schema revision --autogenerate
alembic -n rakuten_schema upgrade head
#alembic -n pinkoi_schema revision --autogenerate
#alembic -n pinkoi_schema upgrade head

#alembic db migrate
#alembic db upgrade
export FLASK_ENV=development
flask run --host="0.0.0.0"
