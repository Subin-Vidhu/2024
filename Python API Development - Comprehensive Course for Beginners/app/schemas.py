from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# Pydantic Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : int = 0

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # Pydantic model to work with ORM

class PostUpdate(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        # orm_mode = True # Pydantic model to work with ORM
        from_attributes = True # Pydantic model to work with ORM

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class createUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)