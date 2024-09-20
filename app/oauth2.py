from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

# tokenUrl takes the endpoint of the login API
oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'login')


# SECRET_KEY
# Algorithm
# Expiration Time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    data_to_encode = data.copy()

    # datetime.datetime.now(datetime.UTC) updated timezone aware | old way: datetime.utcnow() deprecated
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp' : expire})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm = ALGORITHM)
    
    return encoded_jwt  


def verify_access_token(token: str, credentials_exception):

    try:
        payLoad = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id = payLoad.get('user_id')
        user_email = payLoad.get('user_email')

        if user_email is None or user_id is None:
            raise credentials_exception

        # TODO: clarify this line
        token_data = schemas.TokenData(user_id = str(user_id), user_email = user_email)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
# it extracts the user_name and email from the token 
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'Could not verify the creds',
                                         headers = {'WWW-Authenticate': 'Bearer'})
    
    # print(token) gives user_id='37' user_email='test@gmail.com'
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()
    print(user)
    
    return user