from flask_restful import Resource
from models import Product, ProductSchema
from flask import current_app as app
from collections import OrderedDict
from database import Session
from contextlib import contextmanager

# validate, serialize, and deserialize products.
product_schema = ProductSchema()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        Session.remove()

class ProductResource(Resource):
    def get(self, keyword):
        result = OrderedDict()
        result['keyword'] = keyword
        keyword = "%{}%".format(keyword)
        with session_scope() as session:
            product = session.query(Product).filter(Product.name.like(keyword))
            dumped_product = product_schema.dump(product, many=True)
        #app.logger.info(result)
        for product in dumped_product:
            date = product['date']
            product = product['data']['item']
            itemid = product['itemid']
            sellerid = product['shopid']
            name = product['name']
            if result.get(date) is None:
                result[date] = {'total_daily_sold_given_keyword': 0, 'total_daily_avg_price_min_given_keyword': 0.0,
                       'total_daily_avg_price_max_given_keyword': 0.0, 'max_historical_sold': 0, 'daily_hot_seller': None, 'cnt': 0}

            if result[date].get(itemid) is None:
                result[date]['cnt'] += 1
                product_cnt = result[date]['cnt'] # product_cnt 是用來算平均價格，它表示產品的種類數量，跟單一產品種類的數量無關。比如, A產品賣掉5個
                                                       # B產品賣掉6個，則product_cnt是2, 不是11。
                historical_sold = product['historical_sold']
                if historical_sold > result[date]['max_historical_sold']:
                    result[date]['max_historical_sold'] = historical_sold
                    result[date]['daily_hot_seller'] = sellerid
                historical_price_max = product['price_max'] / 100000
                historical_price_min = product['price_min'] / 100000
                result[date]['total_daily_sold_given_keyword'] += historical_sold
                result[date]['total_daily_avg_price_min_given_keyword'] = \
                    result[date]['total_daily_avg_price_min_given_keyword'] * ((product_cnt-1)/product_cnt) + historical_price_min / product_cnt
                result[date]['total_daily_avg_price_max_given_keyword'] = \
                    result[date]['total_daily_avg_price_max_given_keyword'] * ((product_cnt-1)/product_cnt) + historical_price_max / product_cnt
                result[date][itemid] = {'name': name, 'historical_sold': historical_sold, 'historical_price_min': historical_price_min, 'historical_price_max': historical_price_max, 'seller_id': sellerid}

        return result 

class ProductListResource(Resource):
    def get(self):
        with session_scope() as session:
            products = session.query(Product).all()
            dump_result = product_schema.dump(products, many=True)
        return dump_result
