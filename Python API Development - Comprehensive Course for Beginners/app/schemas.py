from pydantic import BaseModel

# Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : int = None