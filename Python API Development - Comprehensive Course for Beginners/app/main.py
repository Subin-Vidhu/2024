from fastapi import FastAPI
from . import models
from .routers import post, users, auth, vote
from .database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# my_post = [{"title": "Post 1", "content": "This is the content of Post 1", "published": True, "rating": 5, "id" : 1},{"title": "Post 2", "content": "This is the content of Post 2", "published": False, "rating": 4, "id" : 2}, {"title": "Post 3", "content": "This is the content of Post 3", "published": True, "rating": 3, "id" : 3}]
# Path Operation decorator/ Route / Endpoint
@app.get("/")
async def root():
    return {"message": "Hello Subin"}

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)