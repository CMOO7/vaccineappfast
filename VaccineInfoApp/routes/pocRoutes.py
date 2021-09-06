from distutils.util import execute
from select import select
from unicodedata import name
from VaccineInfoApp.schemas.users import User
from optparse import Values
from fastapi import APIRouter, FastAPI
from sqlalchemy import insert

from config.db import connection
from models.user import users
from schemas.index import User

userApp = APIRouter()


@userApp.get("/")
async def read_data():
    return connection.execute(users.select()).fetchall()

@userApp.get("/{id}")
async def read_data(id :int):
    return connection.execute(users.select().where(users.c.id == id))

@userApp.post("/")
def write_data(user:User):
    connection.execute(users.insert().values(
        name = user.name,
        password = user.password
    ))
    return connection.execute(users.select()).fetchAll()


# @userApp.get("/")
# async def read_data():
#         return connection.execute(users.select()).fetchall()

# @userApp.get("/")
# async def read_data():
#         return connection.execute(users.select()).fetchall()
