"""
Pydantic schemas for data validation and serialization.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """
    Schema for user output response.
    """
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str

class Token(BaseModel):
    """
    Schema for authentication token.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for token data payload.
    """
    id: Optional[str] = None

class PostBase(BaseModel):
    """
    Base schema for post data.
    """
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    """
    Schema for creating a new post. Inherits from PostBase.
    """
    pass

class Post(PostBase):
    """
    Schema for post response.
    """
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    """
    Schema for post response with vote count.
    """
    Post: Post
    vote: int

    class Config:
        orm_mode = True

class Vote(BaseModel):
    """
    Schema for voting on a post.
    """
    post_id: int
    dir: conint(le=1)