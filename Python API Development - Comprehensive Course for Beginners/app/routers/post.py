from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
import psycopg2
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# # Dependency Injection, testing ORM
# @router.get("/sqlalchemy") 
# def read_sqlalchemy_posts(db: Session = Depends(get_db)):
#     # posts = db.query(models.Post)
#     # print(f"SQLAlchemy Posts: {posts}")
#     # return {"data": "successfully fetched SQLAlchemy posts"}
#     posts = db.query(models.Post).all()
#     return posts


@router.get("/", response_model=list[schemas.Post])
async def read_items(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #return a list of items
    # return {"data" : my_post }

    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # To convert the payload to dictionary
    # payload_dict = payload.dict()
    # payload_dict["id"] = len(my_post) + 1 # Auto Increment ID
    # my_post.routerend(payload_dict)
    # print(f" Pydanctic Model converted to dictionary: {payload_dict}")

    # cursor = connection.cursor()
    # cursor.execute("INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *", (payload.title, payload.content, payload.published, payload.rating)) # RETURNING * is used to return the inserted data, use %s as a placeholder to avoid SQL injection
    # connection.commit() # to save the changes to the database
    # payload_dict = cursor.fetchone()
    # print(f" Pydanctic Model converted to dictionary: {payload}")
    print(f"Current User: {current_user.email}")
    payload_dict = models.Post(owner_id = current_user.id, **payload.dict())
    db.add(payload_dict)
    db.commit()
    db.refresh(payload_dict)
    return payload_dict

# Get the latest post - here order matters so it should be above the //{id}, meaning it should be above the get post by id, an example of a bug is if you try to get the latest post by id, it will not work because it will be treated as an id, eg. //latest will be treated as an id and not as a path to get the latest post 

@router.get("/latest")
async def read_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # return {"data" : my_post[-1]}

    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    # latest_post = cursor.fetchone()

    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post


# Get only one post
@router.get("/{id}", response_model = schemas.Post)
async def read_post(id, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # try:
    #     id = int(id)
    #     return {"data" : my_post[id-1]}
    # # To handle the error of list index out of range
    # except IndexError:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # except:
    #     return {"data" : "Something went wrong"}

    # try:
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    #     post = cursor.fetchone()
    #     if post:
    #         return {"data" : post}
    #     else:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # except (Exception, psycopg2.Error) as error:
    #     print("Error while fetching data from PostgreSQL", error)
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if post:
            return post
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # try:
    #     id = int(id)
    #     deleted_post = my_post.pop(id-1)
    #     return {"data" : f"Post with id {id} is deleted"}
    # except IndexError:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # except:
    #     return {"data" : "Something went wrong"}

    # try:
    #     cursor = connection.cursor()
    #     cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
    #     deleted_post = cursor.fetchone()
    #     connection.commit()
    #     if deleted_post:
    #         return {"data" : f"Post with id {id} is deleted"}
    #     else:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    try:
        posts = db.query(models.Post).filter(models.Post.id == id)
        if posts.first():
            posts.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    except (Exception, psycopg2.Error) as error:
        print("Error while deleting data from PostgreSQL", error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

# Update a post
@router.put("/{id}", response_model=schemas.PostBase)
async def update_post(id, payload: schemas.PostUpdate, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # try:
    #     id = int(id)
    #     my_post[id-1] = payload.dict()
    #     return {"data" : my_post[id-1]}
    # except IndexError:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # except:
    #     return {"data" : "Something went wrong"}

    # try:
    #     cursor = connection.cursor()
    #     cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s returning *", (payload.title, payload.content, payload.published, payload.rating, id))
    #     updated_post = cursor.fetchone()
    #     connection.commit()
    #     if updated_post:
    #         return {"data" : updated_post}
    #     else:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    try:
        posts = db.query(models.Post).filter(models.Post.id == id)
        if posts.first():
            posts.update(payload.dict())
            db.commit()
            return payload
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    except (Exception, psycopg2.Error) as error:
        print("Error while updating data from PostgreSQL", error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        

