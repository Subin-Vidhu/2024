from fastapi import FastAPI

app = FastAPI()

# Path Operation decorator/ Route / Endpoint
@app.get("/")
async def root():
    return {"message": "Hello Subin"}