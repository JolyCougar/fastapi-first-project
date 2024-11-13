# app/schemas.py
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes = True
