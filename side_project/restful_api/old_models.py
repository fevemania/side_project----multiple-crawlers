from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import JSONB

import os
import socket
import psycopg2
from datetime import date
import json
import pdb

orm = SQLAlchemy()
ma = Marshmallow()



class ResourceAddUpdateDelete:
    def add(self, resource):
        orm.session.add(resource)
        return orm.session.commit()
    def update(self):
        return orm.session.commit()
    def delete(self, resource):
        orm.session.delete(resource)
        return orm.session.commit()

class Date(orm.Model, ResourceAddUpdateDelete):
    id = orm.Column(orm.Integer, primary_key=True)
    date = orm.Column(orm.Date(), unique=True, nullable=False)

class Product(orm.Model, ResourceAddUpdateDelete):
#   __abstract__ = True
    id = orm.Column(orm.Integer, primary_key=True)
    data = orm.Column(JSONB, nullable=False)
    name = orm.Column(orm.Text(), nullable=False)
    date = orm.Column(orm.Date())
    #timestamp = orm.Column(orm.DateTime(timezone=True))
    #__table_args__ = (
    #    orm.Index('pgroonga_name_index', name, postgresql_using='pgroonga'),
    #)

    def __init__(self, date, data, name):
        self.date = date
        self.data = data
        self.name = name

class ProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    data = fields.Raw()
    name = fields.String(required=True)
    date = fields.Date()
    #timestamp = fields.AwareDateTime()
    #url = ma.URLFor('service.productresource', id='<id>', _external=True)

class Categories(orm.Model, ResourceAddUpdateDelete):
    id = orm.Column(orm.Integer, primary_key=True)
    category_id = orm.Column(orm.Integer, unique=True, nullable=False)
    category_name = orm.Column(orm.String(50), nullable=False)

    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

class CategoriesSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    category_id = fields.Integer(required=True)
    category_name = fields.String(required=True)

def get_model_by_date(date):
    # date: type str
    class_name, table_name = get_class_name_and_table_name(date)
    cls = type(class_name, (Product, ), {'__tablename__': table_name})
    return cls

def get_class_name_and_table_name(date):
    return 'Product_{}'.format(date), 'product_{}'.format(date)

#POSTGRES_DB = os.environ.get('POSTGRES_DB')
#POSTGRES_USER = os.environ.get('POSTGRES_USER')
#POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
#POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
#POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))
#
#connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
#cursor = connection.cursor()

try:
#   prac = {}
#   prac['key'] = 'value'
#   sql = 'insert into product (data, name, date) VALUES (%s, %s, %s)'
#   cursor.execute(sql, (json.dumps(prac), 'name', date.today()))
#   connection.commit() 
#   cursor.execute('select distinct date from product')
#   result = cursor.fetchall()
    #for row in result:
#    print(type(get_model_by_date(row[0]))== type(Product))
    get_model_by_date('1')
    get_model_by_date('2')
    get_model_by_date('3')
    get_model_by_date('4')
except:
    pdb.set_trace()
    pass

#cursor.close()
#connection.close()
