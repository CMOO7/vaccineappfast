# from importlib.metadata import metadata
# from venv import create
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from mysql.connector import Error, MySQLConnection

# engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/citizenschema")

# connObject = engine.connect()
    


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost:3306/citizenschema"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


