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

# Path Operation decorator/ Route / Endpoint
@app.get("/")
async def root():
    return {"message": "Hello Subin"}

@app.get("/items")
async def read_items():
    #return a list of items
    return [{"item": "item1"}, {"item": "item2"}]

@app.post("/createposts")
async def create_post(payload: Post):
    print(payload.rating)
    # To convert the payload to dictionary
    payload_dict = payload.dict()
    print(f" Pydanctic Model converted to dictionary: {payload_dict}")
    return f"Post created successfully with `Data`: `{payload_dict}`"