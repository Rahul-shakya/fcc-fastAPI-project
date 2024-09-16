from pydantic import BaseModel
from typing import Optional

# this is the pydantic schema

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = False
    
    # optional default values --
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass
