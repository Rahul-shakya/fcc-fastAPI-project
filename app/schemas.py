from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# this is the pydantic schema

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = False
    
    # optional default values --
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass

# response schema
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:

        # this is deprecated
        # orm_mode = True

        # this is new change
        from_attributes = True