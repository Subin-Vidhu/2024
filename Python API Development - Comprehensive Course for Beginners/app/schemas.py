from pydantic import BaseModel

# Pydantic Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : int = None

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    published: bool
    rating : int


    class Config:
        # orm_mode = True # Pydantic model to work with ORM
        from_attributes = True # Pydantic model to work with ORM