from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=schemas.Post)
async def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    # for user specific post: posts = db.query(models.Post).filter(mmodels.Post.owner_id == current_user.id).all()
    return posts


@router.get("/limit", response_model=List[schemas.Post])
async def get_limit_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 5,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .all()
    )  # implement pagination with 'skip|offset' query parameter

    # for user specific post: posts = db.query(models.Post).filter(mmodels.Post.owner_id == current_user.id).all()
    return posts


@router.post(
    "/newpost", status_code=status.HTTP_201_CREATED, response_model=schemas.Post
)
async def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(
        owner_id=current_user.id, **post.dict()
    )  # this avoids having to reference each model column individually
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# bug: failed user verification returns HTTP_404


@router.get(
    "/{id}", response_model=schemas.Post
)  # id is known as a path parameter here
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )
    """
    For user specific post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    """
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_data = post.first()

    # might tweak
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )

    if post_data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    post.delete(synchronize_session=False)
    # return{"message: ": "post successfully deleted"} #preferred

    db.commit()


@router.put("/{id}", response_model=schemas.PostCreate)
async def update_post(
    id: int,
    post_to_update: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    post_query.update(post_to_update.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
