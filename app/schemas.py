from pydantic import BaseModel, EmailStr
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


class UserCreate(BaseModel):

    user_name: str
    email: EmailStr
    password: str

    # we dont include id and created_at because those
    # values are provided by the system and not the user.
    # Here we define only the values which the user will
    # send in the body of the request.


# we dont want to send password back to the user hence including 
# only id and email
class UserOut(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str