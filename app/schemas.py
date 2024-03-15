from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

"""
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #Optional field with default value
    #rating : Optional[int] = None #Optional field that defaults to none
    #user: str

class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class UpPost(BaseModel):
    title: str
    content: str
    #published: bool = True

"""


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # Optional field with default value
    # rating : Optional[int] = None #Optional field that defaults to none
    # user: str

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
    created_at: datetime

    class Config:
        orm_mode = True


class AdminUserRespone(UserResponse):
    pass


class UserLogin(BaseModel):
    # id:int
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    expires: Optional[datetime]
