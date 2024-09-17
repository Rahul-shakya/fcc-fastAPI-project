from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..schemas import UserLogin

# Or we can do from .. import database, and then write Depends(database.get_db)
from ..database import get_db

# done another way
from .. import models
from .. import utils

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid credentials')
    
    # if utils.hash(user_credentials.password) == user.password: 

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid credentials')
    
    # create a token after sucessful authentication
    return {'token' : 'dummy_token'}
     
    
