from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from . import models
import psycopg
from psycopg.rows import dict_row

from sqlalchemy.orm import Session 
from .database import engine, get_db

# we can also import like: from . import schemas(like for models), and then
# we'll have to write schemas.Post everywhere
from .schemas import PostBase, PostCreate

# this line actually creates the tables through SQLAlchemy
models.Base.metadata.create_all(bind = engine)


app = FastAPI()

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
def get_posts(db: Session = Depends(get_db)):

    # without ORMs, directly through SQL statements
    cursor.execute("""SELECT * FROM tb_posts """)
    posts = cursor.fetchall()


@app.post("/create_post", status_code = status.HTTP_201_CREATED)
def create_post(payLoad: PostCreate, db: Session = Depends(get_db)):

    # old deprecated SQL code
    # f-strings are avoided because of security vulnerabilites(SQL injections)
    cursor.execute("""INSERT INTO tb_posts (title, content, is_published, rating) VALUES (%s, %s, %s, %s) RETURNING * """, (payLoad.title, 
                                                                                                        payLoad.content, 
                                                                                                        payLoad.is_published, 
                                                                                                        payLoad.rating))
    new_post = cursor.fetchone()
    conn.commit()

    # implementing code through SQLAlchemy ORMs
    new_post = models.Post(title = payLoad.title, content = payLoad.content, 
                           is_published = payLoad.is_published, rating = payLoad.rating)

    return {"data" : new_post}


@app.get("/posts/{id}")
def get_post_by_id(id : int, db: Session = Depends(get_db)):

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
def delete_post_by_id(id : int, db: Session = Depends(get_db)):
    
    cursor.execute(""" DELETE FROM tb_posts WHERE id = %s RETURNING * """, (id,))
    post_to_del = cursor.fetchone()
    conn.commit()

    if post_to_del.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist')
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post_by_id(id: int, payLoad: PostCreate, db: Session = Depends(get_db)):

    # old deprecated SQL code
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
