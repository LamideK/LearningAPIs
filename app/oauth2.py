from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

#Algo
#Secret key
#Expiration time

SECRET_KEY = '66879DHU9WD820DJ7837TGFP92F380JC329I2P'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithm = ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

#def get_current_user(token:str, Depends):
    