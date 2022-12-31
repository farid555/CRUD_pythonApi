from typing import Optional, List
from fastapi import FastAPI
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import SessionLocal, engine
from .routers import post, user, auth


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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
