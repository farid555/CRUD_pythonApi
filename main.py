from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Welcome to my api..., start nice journey..."}


@app.get("/posts")
def get_posts():
    return {"data": "This is first post"}


@app.post("/posts")
def create_posts(post: Post):
    print(post.dict())
    return {"new_post": post}
