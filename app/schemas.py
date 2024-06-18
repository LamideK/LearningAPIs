from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List
from models import Post, User, Vote


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


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # Optional field with default value
    # rating : Optional[int] = None #Optional field that defaults to none

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class PostOut(PostBase):
    post: List[Post]
    upvotes: int

    class Config:
        from_attributes = True


class OutPost(PostBase):
    title: str
    content: str
    published: bool = True
    id: int
    created_at: datetime
    owner_id: int
    # owner: UserResponse
    upvotes: int

    # orm_model =


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    expires: Optional[datetime] = None

    model_config = ConfigDict(coerce_numbers_to_str=True)


class Vote(BaseModel):
    post_id: int
    dir: bool
