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

    def __init__(self, timestamp, data):
        self.timestamp = timestamp
        self.data = data

class ProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    timestamp = fields.String(required=True)
    data = fields.Raw()
    #url = ma.URLFor('service.productresource', id='<id>', _external=True)
