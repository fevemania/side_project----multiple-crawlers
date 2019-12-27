#!/bin/sh
flask db init
flask db migrate
flask db upgrade
export FLASK_ENV=development
flask run --host="0.0.0.0"
