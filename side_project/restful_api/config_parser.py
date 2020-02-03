import configparser, os
cfg = configparser.ConfigParser()
cfg.read('alembic.ini')
parsing_value = cfg.get('DEFAULT', 'sqlalchemy.shopee.url', vars=os.environ)
cfg.set('DEFAULT', 'sqlalchemy.shopee.url', parsing_value)
parsing_value = cfg.get('DEFAULT', 'sqlalchemy.rakuten.url', vars=os.environ)
cfg.set('DEFAULT', 'sqlalchemy.rakuten.url', parsing_value)
parsing_value = cfg.get('DEFAULT', 'sqlalchemy.pinkoi.url', vars=os.environ)
cfg.set('DEFAULT', 'sqlalchemy.pinkoi.url', parsing_value)

with open('alembic.ini', 'w') as configfile:
    cfg.write(configfile)
