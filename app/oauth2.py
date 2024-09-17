from jose import JWTError, jwt
from datetime import datetime, timedelta


# SECRET_KEY
# Algorithm
# Expiration Time

SECRET_KEY = "a3498d7dbdb98400f5532f588d3ccf317c59e84674888b0ebd8be4f9115313c7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    data_to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp' : expire})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt  