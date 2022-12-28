from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import SessionLocal, engine

from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastApi', user='postgres', password='farid555',
                                cursor_factory=RealDictCursor, )
        cursor = conn.cursor()
        print("DataBase connected successfull!")
        break
    except Exception as error:
        print("Connecting to database failed ")
        print("Error;", error)
        time.sleep(2)


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


@app.get("/sql")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "Success"}


@app.get("/")
def root():
    return {"message": "Welcome to my api..., start nice journey..."}

# Get single


@app.get("/posts/{id}")
def get_posts(id: str):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found...")
       # response.status_code = status.HTTP_404_NOT_FOUND
       # return {"message": f" was not found {id}"}
    return {"post details": post}

# Get all


@app.get("/posts")
def get_posts():
    cursor.execute("""  SELECT * From posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# Create


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    return {"data": new_post}

# Delete


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    print(delete_post)
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Edit


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {"data": updated_post}
