from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True #Optional field with default value
    #rating : Optional[int] = None #Optional field that defaults to none
    #user: str

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True