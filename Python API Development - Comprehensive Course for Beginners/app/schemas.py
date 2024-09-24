from pydantic import BaseModel

# Pydantic Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : int = None

class PostCreate(PostBase):
    pass