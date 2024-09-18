from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schemas import UserLogin

# Or we can do from .. import database, and then write Depends(database.get_db)
from ..database import get_db

# done another way
from .. import models, utils, oauth2

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # OAuth2PasswordRequestForm stores data(username and password) in a dict format
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid credentials')
    
    # if utils.hash(user_credentials.password) == user.password: 

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid credentials')
    
    # create a token after sucessful authentication
    access_token = oauth2.create_access_token(data = {'user_id' : user.id, 'user_email' : user.email})
    
    return {'token' : access_token, "token_type" : "bearer"}
