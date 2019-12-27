from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import orm
from views import service_blueprint


def create_app(config_filename):

    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
    POSTGRES_ADDRESS = socket.gethostbyname(os.environ.get('POSTGRES_HOST'))

    connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_ADDRESS, port=POSTGRES_PORT)
    cursor = connection.cursor()
    cursor.execute('CREATE EXTENSION if not EXISTS pgroonga')
    connection.commit()
    cursor.close()
    connection.close()

    app = Flask(__name__)
    app.config.from_object(config_filename)
    orm.init_app(app)
    app.register_blueprint(service_blueprint, url_prefix='/service')
    migrate = Migrate(app, orm)
    return app


app = create_app('config')
