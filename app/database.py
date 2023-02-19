#for database connection using sql alchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#for database connction using Psycopg2
# import psycopg2
# from psycopg2.extras import RealDictCursor

# import time

# database connection using sqlalchemy --> current

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#database connection with psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database ='fastapi', user = 'postgres', password = 'admin',
#         cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Databse connected")
#         break
#     except Exception as error:
#         print("Database not connected")
#         print("Error was :", error)
#         time.sleep(5)
