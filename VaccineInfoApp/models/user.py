from curses import meta
from sqlalchemy import Integer, Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import  metaObject

users = Table(
    'tbusers', metaObject,
    Column('id',Integer, primary_key=True),
    Column('username',String(255)),
    Column('password', String(255))
)