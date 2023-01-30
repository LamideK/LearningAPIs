from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils #..database import get_db



router = APIRouter(
    tags= ['Authentication']    
)

@router.post('/login')
def login(user_credentials: schemas.UserLogin,db: Session= Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:  
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
        detail=f"login credentials invalid")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
        detail= f"login credentials invalid")

    #generate token
    return{'token': 'example token'}
    # return user
