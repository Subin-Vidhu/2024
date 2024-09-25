from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)
from .routers import post, users, auth

app = FastAPI()

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

# my_post = [{"title": "Post 1", "content": "This is the content of Post 1", "published": True, "rating": 5, "id" : 1},{"title": "Post 2", "content": "This is the content of Post 2", "published": False, "rating": 4, "id" : 2}, {"title": "Post 3", "content": "This is the content of Post 3", "published": True, "rating": 3, "id" : 3}]
# Path Operation decorator/ Route / Endpoint
@app.get("/")
async def root():
    return {"message": "Hello Subin"}

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)