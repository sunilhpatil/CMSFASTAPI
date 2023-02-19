from datetime import datetime
from typing import Optional   
from pydantic import BaseModel, EmailStr, conint

# Class for user creation

class UserCreate(BaseModel):
    email : EmailStr
    password : str   

# class for user response model
class UserOut(BaseModel):
    id: int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True
     
#schema for user login
class UserLogin(BaseModel):
    email : EmailStr
    password : str


# Base model
class PostBase (BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(PostBase):
    pass

# Class for response model
class Post(PostBase):
    id : int
    created_at :datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id : int
    vote_dir : conint(le=1)