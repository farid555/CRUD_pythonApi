from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import SessionLocal, engine, get_db


from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


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


# Get single


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found...")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f" was not found {id}"}
    return post

# Get all


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""  SELECT * From posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

# Create


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
    # print(post.dict())
    new_post = models.Post(**post.dict())
    # or
    # new_post = models.Post(title=post.title, content=post.content,
    # published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# Delete


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(
    # """DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # print(delete_post)
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Edit


@app.put("/posts/{id}")
def updated_post(id: int, newly_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.published, (str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(newly_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
