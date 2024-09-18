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