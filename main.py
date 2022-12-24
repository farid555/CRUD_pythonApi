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


@app.get("/")
def root():
    return {"message": "Welcome to my api..., start nice journey..."}


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id: {id} was not found...")
       # response.status_code = status.HTTP_404_NOT_FOUND
       # return {"message": f" was not found {id}"}
    return {"post details": post}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}
