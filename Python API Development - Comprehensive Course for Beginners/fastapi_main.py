from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()

# Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : int = None

my_post = [{"title": "Post 1", "content": "This is the content of Post 1", "published": True, "rating": 5, "id" : 1},{"title": "Post 2", "content": "This is the content of Post 2", "published": False, "rating": 4, "id" : 2}, {"title": "Post 3", "content": "This is the content of Post 3", "published": True, "rating": 3, "id" : 3}]
# Path Operation decorator/ Route / Endpoint
@app.get("/")
async def root():
    return {"message": "Hello Subin"}

@app.get("/posts")
async def read_items():
    #return a list of items
    return {"data" : my_post }

@app.post("/posts")
async def create_post(payload: Post):
    # To convert the payload to dictionary
    payload_dict = payload.dict()
    payload_dict["id"] = len(my_post) + 1 # Auto Increment ID
    my_post.append(payload_dict)
    print(f" Pydanctic Model converted to dictionary: {payload_dict}")
    return f"Post created successfully with `Data`: `{payload_dict}`"

# Get only one post
@app.get("/posts/{id}")
async def read_post(id: int):
    try:
        return {"data" : my_post[id-1]}
    except:
        return {"data" : "Post not found"}