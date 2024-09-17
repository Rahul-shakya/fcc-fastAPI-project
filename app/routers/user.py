#                                                                        #
# ------------------------------ USER -----------------------------------#
#                                                                        #

# we can also import like: from ..schemas import Post (like for models above), and then
# we'll have to write only Post everywhere
# did it the other way
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

# importing error
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session 
from ..database import get_db

router = APIRouter(
    prefix = "/users"
)

# USER REGISTRATION
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())

    # hash the password
    password_hash = utils.hash(new_user.password)
    new_user.password = password_hash

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except IntegrityError as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Email already exists.")
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Unexpected error.')


    return new_user

# USER GET
@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id: {id} not found')
    
    return user