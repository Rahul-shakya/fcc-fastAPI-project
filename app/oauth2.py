from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas

# tokenUrl takes the endpoint of the login API
oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'login')


# SECRET_KEY
# Algorithm
# Expiration Time

SECRET_KEY = "a3498d7dbdb98400f5532f588d3ccf317c59e84674888b0ebd8be4f9115313c7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    

def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'Could not verify the creds',
                                         headers = {'WWW-Authenticate': 'Bearer'})
    
    return verify_access_token(token, credentials_exception)