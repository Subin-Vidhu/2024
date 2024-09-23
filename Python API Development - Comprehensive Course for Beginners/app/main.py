from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
import time
from psycopg2.extras import RealDictCursor
app = FastAPI()
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


# Database Connection
def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="FASTAPI",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor
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

# Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : int = None

# Dependency Injection, testing ORM
@app.get("/sqlalchemy") 
def read_sqlalchemy_posts(db: Session = Depends(get_db)):
    # posts = db.query(models.Post)
    # print(f"SQLAlchemy Posts: {posts}")
    # return {"data": "successfully fetched SQLAlchemy posts"}
    posts = db.query(models.Post).all()
    return {"data": posts}

# my_post = [{"title": "Post 1", "content": "This is the content of Post 1", "published": True, "rating": 5, "id" : 1},{"title": "Post 2", "content": "This is the content of Post 2", "published": False, "rating": 4, "id" : 2}, {"title": "Post 3", "content": "This is the content of Post 3", "published": True, "rating": 3, "id" : 3}]
# Path Operation decorator/ Route / Endpoint
@app.get("/")
async def root():
    return {"message": "Hello Subin"}

@app.get("/posts")
async def read_items():
    #return a list of items
    # return {"data" : my_post }
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(payload: Post):
    # To convert the payload to dictionary
    # payload_dict = payload.dict()
    # payload_dict["id"] = len(my_post) + 1 # Auto Increment ID
    # my_post.append(payload_dict)
    # print(f" Pydanctic Model converted to dictionary: {payload_dict}")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *", (payload.title, payload.content, payload.published, payload.rating)) # RETURNING * is used to return the inserted data, use %s as a placeholder to avoid SQL injection
    connection.commit() # to save the changes to the database
    payload_dict = cursor.fetchone()
    return {"data": payload_dict}

# Get the latest post - here order matters so it should be above the /posts/{id}, meaning it should be above the get post by id, an example of a bug is if you try to get the latest post by id, it will not work because it will be treated as an id, eg. /posts/latest will be treated as an id and not as a path to get the latest post 

@app.get("/posts/latest")
async def read_latest_post():
    # return {"data" : my_post[-1]}
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    latest_post = cursor.fetchone()
    return {"data" : latest_post}


# Get only one post
@app.get("/posts/{id}")
async def read_post(id, response: Response):
    # try:
    #     id = int(id)
    #     return {"data" : my_post[id-1]}
    # # To handle the error of list index out of range
    # except IndexError:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # except:
    #     return {"data" : "Something went wrong"}
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()
        if post:
            return {"data" : post}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id, response: Response):
    # try:
    #     id = int(id)
    #     deleted_post = my_post.pop(id-1)
    #     return {"data" : f"Post with id {id} is deleted"}
    # except IndexError:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # except:
    #     return {"data" : "Something went wrong"}
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
        deleted_post = cursor.fetchone()
        connection.commit()
        if deleted_post:
            return {"data" : f"Post with id {id} is deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    except (Exception, psycopg2.Error) as error:
        print("Error while deleting data from PostgreSQL", error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

# Update a post
@app.put("/posts/{id}")
async def update_post(id, payload: Post, response: Response):
    # try:
    #     id = int(id)
    #     my_post[id-1] = payload.dict()
    #     return {"data" : my_post[id-1]}
    # except IndexError:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # except:
    #     return {"data" : "Something went wrong"}
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s returning *", (payload.title, payload.content, payload.published, payload.rating, id))
        updated_post = cursor.fetchone()
        connection.commit()
        if updated_post:
            return {"data" : updated_post}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    except (Exception, psycopg2.Error) as error:
        print("Error while updating data from PostgreSQL", error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        