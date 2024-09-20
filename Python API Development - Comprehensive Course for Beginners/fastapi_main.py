from fastapi import FastAPI

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
async def create_post():
    return {"message": "Post has been created successfully"}