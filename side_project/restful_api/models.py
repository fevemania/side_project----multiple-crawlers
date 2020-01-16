from sqlalchemy import Table, Column, Integer, String, Date, Text, Sequence
from sqlalchemy.orm import mapper
from database import metadata, db_session
from sqlalchemy.dialects.postgresql import JSONB

class Product(object):
    query = db_session.query_property()

    def __init__(self, date, name, data):
        self.date = date
        self.name = name
        self.data = data
    
    def __repr__(self):
        return '<Product {}, {}'.format(self.date, self.name)

product = Table('product', metadata, 
    #Column('id', Integer, Sequence('product_id_seq'), primary_key=True),
    Column('id', Integer, primary_key=True),
    Column('date', Date, nullable=False, primary_key=True),
    Column('name', Text, nullable=False),
    Column('data', JSONB, nullable=False),
    postgresql_partition_by='range(date)'
)
mapper(Product, product)

