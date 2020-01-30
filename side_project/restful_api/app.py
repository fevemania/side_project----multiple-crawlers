from flask import Flask, Blueprint
from flask_restful import Api
#from pinkoi.views import ProductResource, ProductListResource
from rakuten.views import ProductResource, ProductListResource
import os
import socket
import psycopg2

def create_app():
    app = Flask(__name__)
    service_blueprint = Blueprint('service', __name__)
    # link Api to Blueprint
    service = Api(service_blueprint)
    service.add_resource(ProductListResource, '/products/')
    service.add_resource(ProductResource, 
            '/products/<string:keyword>')
    #       '/products/<string:keyword>/from=<string:start_date>',
    #       '/products/<string:keyword>/to=<string:end_date>',
    #       '/products/<string:keyword>/from=<string:start_date>/to=<string:end_date>')
    app.register_blueprint(service_blueprint, url_prefix='/service')

    return app


app = create_app()
