from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    tags= ['Posts']
)

@router.get('/posts', response_model= List[schemas.Post])
async def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/newpost', status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db)):
    new_post = models.Post(**post.dict()) #this avoids having to reference each model column individually
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/posts/{id}', response_model= schemas.Post) #id is known as a path parameter here
async def get_post(id: int, db: Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:  
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} not found")
    return post

@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,  db: Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

# might tweak
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
     #return{"message: ": "post successfully deleted"} #preferred
    post.delete(synchronize_session= False) 
    db.commit()


@router.put('/posts/{id}', response_model= schemas.PostCreate)
async def update_post(id: int, post_to_update: schemas.PostCreate, db: Session= Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    post_query.update(post_to_update.dict(), synchronize_session= False)
    db.commit()

    return post_query.first()
