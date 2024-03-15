from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import asyncio


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Algo
# Secret key
# Expiration time

SECRET_KEY = "66879DHU9WD820DJ7837TGFP92F380JC329I2P"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


def create_access_token(data: dict):
    data_to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        expires = payload.get("exp")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


"""
    
        if expires is None:
            raise credentials_exception
        if datetime.utcnow() > token_data.expires:
            raise credentials_exception
"""


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = await verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
    # getattr(token, "id")


"""
def create_access_token(data: dict, expires_delta: timedelta):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    data_to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
"""
