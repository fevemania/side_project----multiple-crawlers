from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import socket

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST', 'localhost'))

SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=POSTGRES_USER, 
        DB_PASS=POSTGRES_PASSWORD, DB_ADDR=POSTGRES_ADDRESS, DB_NAME=POSTGRES_DB)
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(bind=engine))

#def init_db():
#    metadata.create_all(bind=engine)

