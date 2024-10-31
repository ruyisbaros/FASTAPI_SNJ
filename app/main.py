import time
from random import randrange
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Request, Response, status
from psycopg2.extras import RealDictCursor

# from fastapi.params import Body
from pydantic import BaseModel

# LOCAL SERVER
app = FastAPI()

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


my_posts2 = []


########## GET ALL POSTS ##########
###################################
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    my_posts = cursor.fetchall()
    # print(my_posts)
    return {"data": my_posts}


######### CREATE A NEW POST #########
#####################################
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute(
        """insert into posts (title, content, published) values(%s, %s, %s) returning *""",
        (new_post.title, new_post.content, new_post.published),
    )
    new_post = cursor.fetchone()

    conn.commit()

    return {"message": "New post created successfully", "data": new_post}


######### GET A POST WITH RELEVANT ID #################
#######################################################
@app.get("/posts/{id}")
def get_post(id: int, res: Response):
    print(id)
    print(type(id))
    try:
        # Attempt to retrieve the post from the 'database'
        cursor.execute(
            """SELECT * FROM posts WHERE post_id = %s""",
            (str(id)),
        )
        post = cursor.fetchone()

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
def delete_post(id: int):
    try:
        cursor.execute(
            """DELETE FROM posts WHERE post_id = %s returning * """,
            (str(id)),
        )
        post = cursor.fetchone()
        if post is None:
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


###### UPDATE A POST WITH RELEVANT ID #################
#######################################################
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: Post):
    try:
        cursor.execute(
            """update posts set title=%s WHERE post_id = %s returning * """,
            (updated_post.title, str(id)),
        )
        post = cursor.fetchone()

        if post is None:  # Check if the post exists
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        conn.commit()
        # post.update(updated_post_dict)
        return {"message": "Post updated successfully", "data": post}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
