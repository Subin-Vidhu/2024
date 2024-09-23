from sqlalchemy import create_engine # to create a database engine
from sqlalchemy.ext.declarative import declarative_base # to create a base class
from sqlalchemy.orm import sessionmaker # to create a session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/FASTAPI" # Database URL
 
engine = create_engine(SQLALCHEMY_DATABASE_URL) # create a database engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create a session

Base = declarative_base() # create a base class