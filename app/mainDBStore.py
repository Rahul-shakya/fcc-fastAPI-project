from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from . import models
import psycopg
from psycopg.rows import dict_row

from sqlalchemy.orm import Session 
from .database import engine, get_db

# this line actually creates the tables through SQLAlchemy
models.Base.metadata.create_all(bind = engine)


class Post(BaseModel):
    title: str
    content: str
    
    # optional default values --
    is_published: bool = False
    rating: Optional[int] = None

class DataStore():
    def __init__(self):
        self.posts = []

    def add_post(self, post):
        self.posts.append(post)

    def return_posts(self):
        return self.posts
    
    def curr_length(self):
        return len(self.posts)
    
    def find_post_by_id(self, id):
        for curr_post in self.posts:
            print(curr_post)
            if id == curr_post['id']:
                return curr_post
        return None

app = FastAPI()

postsObj = DataStore()

conn_params = {
    "dbname": "postsDB",
    "user": "admin",
    "password": "admin",
    "host": "localhost"  
}

# setting up connection with the db
try:
    conn = psycopg.connect(**conn_params, row_factory = dict_row)

    cursor = conn.cursor()
    print('DB connection successful.')
except Exception as error:
    print(f'failed. Error: {error}')


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM tb_posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"posts_data" : posts}


@app.post("/create_post")
def create_post(payLoad: Post):

    # f-strings are avoided because of security vulnerabilites(SQL injections)
    cursor.execute("""INSERT INTO tb_posts (title, content, is_published, rating) VALUES (%s, %s, %s, %s) RETURNING * """, (payLoad.title, 
                                                                                                        payLoad.content, 
                                                                                                        payLoad.is_published, 
                                                                                                        payLoad.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}

    return True


@app.get("/posts/{id}")
def get_post_by_id(id : int):
    # this also works: with type casting it to str
    # cursor.execute(""" SELECT * FROM tb_posts WHERE id = %s """, (str(id),))

    cursor.execute(""" SELECT * FROM tb_posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f'Post with id: {id} not found')

    print(post)
    return {"post_data" : post}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id : int):
    
    cursor.execute(""" DELETE FROM tb_posts WHERE id = %s RETURNING * """, (id,))
    post_to_del = cursor.fetchone()
    conn.commit()

    if post_to_del is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist')
    
    print(f'Post ID to delete: {post_to_del['id']}')

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post_by_id(id: int, payLoad: Post):
    
    cursor.execute(""" UPDATE tb_posts SET title = %s, content = %s, is_published = %s, 
                   rating = %s  WHERE id = %s RETURNING *""", (payLoad.title, payLoad.content, 
                                                               payLoad.is_published, 
                                                               payLoad.rating,
                                                               id))
    post_to_update = cursor.fetchone()
    conn.commit()

    if post_to_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist. Unable to update!')
    
    return {'message' : post_to_update}


@app.get("/test/sqlalc")
def test_posts(db: Session = Depends(get_db)):
    return {'msg': 'success'}
