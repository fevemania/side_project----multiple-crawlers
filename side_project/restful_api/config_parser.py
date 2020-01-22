import configparser, os
cfg = configparser.ConfigParser()
cfg.read('alembic.ini')
parsing_value = cfg.get('DEFAULT', 'sqlalchemy.url', vars=os.environ)
cfg.set('DEFAULT', 'sqlalchemy.url', parsing_value)

with open('alembic.ini', 'w') as configfile:
    cfg.write(configfile)
