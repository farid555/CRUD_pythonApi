from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "this the first content", "id": 1},
            {"title": "title of post 2", "content": "this the second content", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def delete_index_post(id):
    for index, p in enumerate(my_posts):
        if p["id"] == id:
            return index


@app.get("/")
def root():
    return {"message": "Welcome to my api..., start nice journey..."}

# Get single


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id: {id} was not found...")
       # response.status_code = status.HTTP_404_NOT_FOUND
       # return {"message": f" was not found {id}"}
    return {"post details": post}

# Get all


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Create


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}

# Delete


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    indexDelete = delete_index_post(id)
    if indexDelete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    my_posts.pop(indexDelete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Edit


@app.put("/posts/{id}")
def updat_post(id: int, post: Post):
    index_put = delete_index_post(id)
    if index_put == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index_put] = post_dict
    return {"data": post_dict}