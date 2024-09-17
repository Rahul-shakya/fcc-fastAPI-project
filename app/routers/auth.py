from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..schemas import UserLogin

# Or we can do from .. import database, and then write Depends(database.get_db)
from ..database import get_db

# done another way
from .. import models, utils, oauth2

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
    
    access_token = oauth2.create_access_token(data = {'user_id' : user.id, 'user_email' : user.email})
    # create a token after sucessful authentication
    return {'token' : access_token, "token_type" : "bearer"}
    
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozNywidXNlcl9lbWFpbCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNzI2NTk1NTQ0fQ.PStMc2fzSuvlk-eIWztvYF29TqKBLgQTp3cG7s2ytH8
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozNywiZXhwIjoxNzI2NTk1NTc2fQ.BKens4G8i8p1fnhGL7i-eQgbjFs6a2XAhJtJsL1K-L8