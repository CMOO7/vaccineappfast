from importlib.metadata import metadata
from sqlalchemy import create_engine, MetaData

DATABASE_MYSQL_URL = 'mysql+pymysql://root@localhost:3306/citizenschema'

engine = create_engine(DATABASE_MYSQL_URL)

metaObject = MetaData()
connection = engine.connect()

