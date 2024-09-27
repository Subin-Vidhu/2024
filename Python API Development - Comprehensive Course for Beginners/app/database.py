from sqlalchemy import create_engine # to create a database engine
from sqlalchemy.ext.declarative import declarative_base # to create a base class
from sqlalchemy.orm import sessionmaker # to create a session
import psycopg2 # to connect to PostgreSQL
import time # to sleep the program for a few seconds
from psycopg2.extras import RealDictCursor # to return the data as a dictionary, by default it returns as a list of tuples, ie to return the data in key value pairs, ie to have the column name as the key and the value as the value


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/FASTAPI" # Database URL
 
engine = create_engine(SQLALCHEMY_DATABASE_URL) # create a database engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create a session

Base = declarative_base() # create a base class

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Connection
def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="FASTAPI",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor # to return the data as a dictionary, by default it returns as a list of tuples, ie to return the data in key value pairs, ie to have the column name as the key and the value as the value
        )
        print("Connection to PostgreSQL is successful")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

# check if the connection is successful
while True:
    connection = get_connection()
    if connection:
        break
    else:
        print("Connection failed, retrying...")
        time.sleep(5)
        continue