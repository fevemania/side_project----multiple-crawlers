from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from http_status import HttpStatus
from models import orm, Product, ProductSchema
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app as app
from sqlalchemy import func

service_blueprint = Blueprint('service', __name__)
# validate, serialize, and deserialize products.
product_schema = ProductSchema()
# link Api to Blueprint
service = Api(service_blueprint)

class ProductResource(Resource):
    def get(self, keyword):
        keyword = "%{}%".format(keyword)
        #product = Product.query.filter(Product.data['item']['name'].like(keyword)).first()
        product = Product.query.filter(Product.data['item']['name'].astext.like(keyword))
        #app.logger.info(result)
        dumped_product = product_schema.dump(product, many=True).data
        result = {} 
        for product in dumped_product:
            name = product['data']['item']['name']
            timestamp = product['timestamp']
            if result.get(name) is None:
                result[name] = {'history price': {}, 'history volumes': {}, 'daily volumes': {}, 'daily avg price': {}, 'hot seller': {}}
            result[name]['history price'][timestamp] = name

        return result 

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        dump_result = product_schema.dump(products, many=True).data
        return dump_result

service.add_resource(ProductListResource,
    '/products/')
service.add_resource(ProductResource,
    '/products/<string:keyword>')
