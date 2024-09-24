from pydantic import BaseModel
from datetime import datetime
# Pydantic Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : int = None

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id: int
    title: str
    published: bool
    rating : int
    created_at: datetime

    class Config:
        # orm_mode = True # Pydantic model to work with ORM
        from_attributes = True # Pydantic model to work with ORM