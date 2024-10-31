import time
from random import randrange
from typing import Optional

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor

# from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

# LOCAL SERVER
app = FastAPI()

# RUNS ORM
models.Base.metadata.create_all(bind=engine)


# POSTGRES DB CONNECT
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi_snj",
            user="postgres",
            password="ahmet",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection established successfully")
        break

    except (Exception, psycopg2.DatabaseError) as e:
        print("Error with connecting to database")
        print("Error: %s" % e)
        time.sleep(2)


class Post(BaseModel):
    # id: int
    title: str
    content: str
    published: bool = True


########## GET ALL POSTS ##########
###################################
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    my_posts = db.query(models.Post).all()
    return {"data": my_posts}


######### CREATE A NEW POST #########
#####################################
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "New post created successfully", "data": new_post}


######### GET A POST WITH RELEVANT ID #################
#######################################################
@app.get("/posts/{id}")
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
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
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
        return {"message": "Post updated successfully", "data": post_query.first()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
