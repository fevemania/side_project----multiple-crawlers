from sqlalchemy import Table, Column, Integer, String, Date, Text, Sequence, Index, ForeignKey, Float
from sqlalchemy.orm import mapper
from pinkoi.database import metadata, Session
from sqlalchemy.dialects.postgresql import JSONB
from marshmallow import Schema, fields

class Product(object):
    def __init__(self, date, name, data):
        self.date = date
        self.name = name
        self.data = data
    
    def __repr__(self):
        return '<Product {}, {}'.format(self.date, self.name)

class Dates(object):
    pass

class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    currency = fields.String(required=True)
    price = fields.Integer(required=True)
    name = fields.String(required=True)

# CREATE TABLE product (
#  id SERIAL NOT NULL,
#  date DATE NOT NULL,
#  name TEXT NOT NULL,
#  data JSONB NOT NULL,
#  PRIMARY KEY (id, date)
# ) PARTITION BY range(date);

product = Table('product', metadata, 
    Column('id', Integer, autoincrement=True, unique=False, primary_key=True),
    Column('date', Date, nullable=False, primary_key=True),
    Column('currency', Text, nullable=False),
    Column('price', Float, nullable=False),
    Column('name', Text, nullable=False),
    Index('pgroonga_name_index', 'name', postgresql_using='pgroonga'),
    postgresql_partition_by='range(date)'
)

dates = Table('dates', metadata,
    Column('date', Date, nullable=False, primary_key=True)
)

mapper(Product, product)
mapper(Dates, dates)
