from sqlalchemy import Table, Column, Integer, String, Date, Text, Sequence, Index, ForeignKey, Float, BigInteger
from sqlalchemy.orm import mapper
from shopee.database import metadata, Session
from sqlalchemy.dialects.postgresql import JSONB
from marshmallow import Schema, fields

class Product(object):
    def __init__(self, date, name, itemid, sellerid, historical_sold, price_max, price_min):
        self.date = date
        self.name = name
        self.itemid = itemid
        self.sellerid = sellerid
        self.historical_sold = historical_sold
        self.price_max = price_max
        self.price_min = prcie_min
        #self.data = data
    
    def __repr__(self):
        return '<Product {}, {}'.format(self.date, self.name)

class Dates(object):
    pass

class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    name = fields.String(required=True)
    itemid = fields.Integer()
    sellerid = fields.Integer()
    historical_sold = fields.Integer()
    price_max = fields.Float()
    price_min = fields.Float()
   #data = fields.Raw()

class Category(object):
    def __init__(self, id, name):
        self.id = id
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
    Column('name', Text, nullable=False),
    Column('itemid', BigInteger, nullable=False),
    Column('sellerid', BigInteger, nullable=False),
    Column('historical_sold', Integer, nullable=False),
    Column('price_max', Float),
    Column('price_min', Float),
    #Column('data', JSONB, nullable=False),
    Index('pgroonga_name_index', 'name', postgresql_using='pgroonga'),
    postgresql_partition_by='range(date)'
)

dates = Table('dates', metadata,
    Column('date', Date, nullable=False, primary_key=True)
)

category = Table('category', metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('name', String(50), nullable=False)
)

mapper(Product, product)
mapper(Dates, dates)
mapper(Category, category)
