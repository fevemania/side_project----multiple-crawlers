from sqlalchemy import Table, Column, Integer, String, Date, Text, Index, Float, Boolean
from sqlalchemy.orm import mapper
from rakuten.database import metadata, Session
from sqlalchemy.dialects.postgresql import JSONB
from marshmallow import Schema, fields

class Product(object):
    def __init__(self, date, currency, price_min, price_max, name, shope_id, shope_name):
        self.date = date
        self.currency = currency
        self.price_min = price_min
        self.price_max = price_max
        self.name = name
        self.shop_id = shop_id
        self.shop_name = shop_name
    
    def __repr__(self):
        return '<Product {}, {}'.format(self.date, self.name)

class Dates(object):
    pass

class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    currency = fields.String(required=True)
    price_min = fields.Float()
    price_max = fields.Float()
    name = fields.String(required=True)
    shop_id = fields.String(required=True)
    shop_name = fields.String(required=True)

class Category(object):
    def __init__(self, id, level, is_leaf_node, page_count, name):
        self.id = id
        self.level = level
        self.is_leaf_node = is_leaf_node
        self.page_count = page_count
        self.name = name

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
    Column('currency', String(50), nullable=False),
    Column('price_min', Float),
    Column('price_max', Float),
    Column('name', Text, nullable=False),
    Column('shop_id', Text, nullable=False),
    Column('shop_name', Text, nullable=False),
    Index('pgroonga_name_index', 'name', postgresql_using='pgroonga'),
    postgresql_partition_by='range(date)'
)

dates = Table('dates', metadata,
    Column('date', Date, nullable=False, primary_key=True)
)

category = Table('category', metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('level', Integer, nullable=False),
    Column('is_leaf_node', Boolean, nullable=False),
    Column('page_count', Integer, nullable=False),
    Column('name', String(50), nullable=False)
)

mapper(Product, product)
mapper(Dates, dates)
mapper(Category, category)
