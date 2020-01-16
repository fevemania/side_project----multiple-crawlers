import os
import socket
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ECHO = False
SQLAlCHEMY_TRACK_MODIFICATIONS = True
address = socket.gethostbyname(os.environ.get('POSTGRES_HOST', 'localhost'))
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="admin", DB_PASS="mypass", DB_ADDR=address, DB_NAME="db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
