from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
import json
from pydantic import parse_obj_as
from typing import List, Optional, Any
from sqlalchemy.orm import Session, join
from sqlalchemy import func, outerjoin, select, values, label, inspect
import models, schemas, oauth2
from database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])

"""
def JSONify(xx):
    formatted_results = []
    for post, upvotes in xx:
        xx_dict = xx.__dict__ 
        xx_dict["upvotes"] = upvotes
        formatted_results.append(xx_dict)
        print(formatted_results)

    return parse_obj_as(List[schemas.OutPost], formatted_results)
"""


@router.get("/")  # Endpoint 100% needs to be optimized
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    posts = db.query(models.Post).all()
    # for user specific post: posts = db.query(models.Post).filter(mmodels.Post.owner_id == current_user.id).all()

    result = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("upvotes"),
        )
        .outerjoin(models.Vote)
        .filter(models.Vote.post_id == models.Post.id)
        .group_by(models.Post.id)
        .all()
    )

    formatted_results = []
    for post, upvotes in result:
        post_dict = post.__dict__
        post_dict["upvotes"] = upvotes
        formatted_results.append(post_dict)
        print(formatted_results)
    return parse_obj_as(List[schemas.OutPost], formatted_results)


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


@router.get("/{id}")  # id is known as a path parameter here
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    result = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("upvotes"),
        )
        .outerjoin(models.Vote)
        .filter(models.Vote.post_id == models.Post.id)
        .group_by(models.Post.id)
        .all()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )

    formatted_results = []
    for post, upvotes in result:
        post_dict = post.__dict__
        post_dict["upvotes"] = upvotes
        formatted_results.append(post_dict)
    return formatted_results

    # Consider a different method/function for optimization

    """
    

    For user specific post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    """

    return parse_obj_as(List[schemas.OutPost], formatted_results)  # post


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
