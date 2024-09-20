from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from pydantic.types import conint
from typing_extensions import Annotated

# this is the pydantic schema

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = False
    
    # optional default values --
    rating: Optional[int] = None


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


# we wont be adding user_id in PostCreate because we will get the
# user_id by application code logic rather than sending it in the
# body
class PostCreate(PostBase):
    pass

# response schema
class Post(PostBase):
    id: int
    created_at: datetime

    # added foriegn key column user_id
    user_id: int
    user: UserOut 

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




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    user_email: Optional[str] = None


class Like(BaseModel):
    post_id: int

    # this allows direction to only hold values >= 0 and <= 1 
    # TODO: Find an enum solution
    direction: Annotated[int, Field(strict=True, le = 1, ge = 0)]