from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import JSONB

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

class Product(orm.Model, ResourceAddUpdateDelete):
    id = orm.Column(orm.Integer, primary_key=True)
    timestamp = orm.Column(orm.String(250), nullable=False)
    data = orm.Column(JSONB, nullable=False)
    name = orm.Column(orm.Text(), nullable=False)
    __table_args__ = (
        orm.Index('pgroonga_name_index', name, postgresql_using='pgroonga'),
    )

    def __init__(self, timestamp, data, name):
        self.timestamp = timestamp
        self.data = data
        self.name = name

class ProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    timestamp = fields.String(required=True)
    data = fields.Raw()
    name = fields.String(required=True)
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
