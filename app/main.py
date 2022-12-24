from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
import psycopg
import psycopg_binary
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

#from psycopg2.extras import RealDictCursor
#from psycopg_binary.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#connect to the database 
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database= 'FASTAPI', user= 'postgres', password= 'passw0rd', cursor_factory= RealDictCursor)  #, cursor_factory= RealDictCursor
        cursor = conn.cursor()
        print('Successful')
        break
    except Exception as e:
        print('Error: ', e)
        time.sleep(4) #Best for testing against internet problems, not authentication


@app.get('/') # this is called a decorator
async def root():
    return {"message": "Hello..."}

@app.get('/posts', response_model= List[schemas.Post])
async def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/newpost', status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db)):
    new_post = models.Post(**post.dict()) #this avoids having to reference each model column individually
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{id}', response_model= schemas.Post) #id is known as a path parameter here
async def get_post(id: int, db: Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:  
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} not found")
    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,  db: Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

# might tweak
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
     #return{"message: ": "post successfully deleted"} #preferred
    post.delete(synchronize_session= False) 
    db.commit()


@app.put('/posts/{id}', response_model= schemas.Post)
async def update_post(id: int, post_to_update: schemas.PostCreate, db: Session= Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    post_query.update(post_to_update.dict(), synchronize_session= False)
    db.commit()

    return post_query.first()
