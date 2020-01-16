from models import Product, orm
import os
import socket
import psycopg2

def get_model_by_date(date):
    # date: type str
    class_name, table_name = get_class_name_and_table_name(date)
    cls = type(class_name, (Product, ), {'__tablename__': table_name})
    return cls

def get_class_name_and_table_name(date):
    return 'Product_{}'.format(date), 'product_{}'.format(date)

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
cursor = connection.cursor()

cursor.execute('select distinct date from product')
result = cursor.fetchall()
for row in result:
    get_model_by_date(row[0])

orm.create_all()

cursor.close()
connection.close()
