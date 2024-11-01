from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])


########## GET ALL USERS ##########
@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    my_users = db.query(models.User).all()
    return my_users


##### GET A USER FROM  THE DATABASE BY ID #####
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()

        if user is None:
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"An error occurred: {str(e)}",
        )


########## CREATE  A USER ##########
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user is already existing
        userchk = (
            db.query(models.User).filter(models.User.email == user["email"]).first()
        )
        if userchk is not None:
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User already exist"
            )
        # hash the password
        hashed_pwd = get_password_hash(user.password)
        user.password = hashed_pwd
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


########### UPDATE A USER #############
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user(
    id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)
):
    try:
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()  # Fetch the user from the database
        if user is None:  # Check if the user exists
            # Raise a 404 error if the user does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user_query.update(updated_user.model_dump(), synchronize_session=False)
        db.commit()
        return user_query.first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
