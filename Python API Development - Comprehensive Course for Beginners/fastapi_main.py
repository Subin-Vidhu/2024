from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()

# Path Operation decorator/ Route / Endpoint
@app.get("/")
async def root():
    return {"message": "Hello Subin"}

@app.get("/items")
async def read_items():
    #return a list of items
    return [{"item": "item1"}, {"item": "item2"}]

@app.post("/createposts")
async def create_post(payload: dict = Body(...)):
    print(payload)
    return {"message": "Post has been created successfully"}