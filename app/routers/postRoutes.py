from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


########## GET ALL POSTS ##########
###################################
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    my_posts = db.query(models.Post).all()
    return my_posts


######### CREATE A NEW POST #########
#####################################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


######### GET A POST WITH RELEVANT ID #################
#######################################################
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()

        if post is None:
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        return post
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


###### DELETE A POST WITH RELEVANT ID #################
#######################################################
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()  # Fetch the post from the database
        if post is None:
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


###### UPDATE A POST WITH RELEVANT ID #################
#######################################################
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()  # Fetch the post from the database
        if post is None:  # Check if the post exists
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        post_query.update(updated_post.model_dump(), synchronize_session=False)
        db.commit()
        return post_query.first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
