from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Response, status

# from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    # id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "Inside post ",
        "content": "Inside post content",
        "published": True,
        "rating": 3,
        "id": 1,
    }
]


@app.get("/")
def hello():
    return {"message": "Hello, world and ahmet!"}


# Get All Posts
@app.get("/posts")
def get_posts():
    return {"message": "New post created successfully", "posts": my_posts}


# Create a new Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    new_post = new_post.model_dump()
    new_post["id"] = randrange(0, 1_000_000)
    my_posts.append(new_post)
    return {"message": "New post created successfully", "new post": new_post}


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            print("Found post with")
            return p


# Get post with relevant id
@app.get("/posts/{id}")
def get_post(id: int, res: Response):
    print(id)
    print(type(id))
    try:
        # Attempt to retrieve the post from the 'database'
        post = find_post(id)
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


# Delete post with  relevant id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        post = find_post(id)
        if post is None:
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        my_posts.remove(post)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


# Update  post with relevant id
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: Post):
    try:
        post = find_post(id)
        if post is None:
            # Raise a 404 error if the post does not exist
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        updated_post_dict = updated_post.model_dump()
        post.update(updated_post_dict)
        return {"message": "Post updated successfully", "updated post": post}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
