from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True #Optional field with default value
    #rating : Optional[int] = None #Optional field that defaults to none
    #user: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime


    class Config:
        orm_mode = True