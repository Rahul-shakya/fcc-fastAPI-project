from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from . import models
import psycopg
from psycopg.rows import dict_row
from typing import List

from sqlalchemy.orm import Session 
from .database import engine, get_db

# we can also import like: from . import schemas(like for models above), and then
# we'll have to write schemas.Post everywhere
from .schemas import *

# if done the other way, we'll call hash function as utils.hash(password)
from .utils import hash


# importing error
from sqlalchemy.exc import IntegrityError

# this line actually creates the tables through SQLAlchemy
models.Base.metadata.create_all(bind = engine)


app = FastAPI()

# return type is a list of Posts, hence response_model is a list of posts
@app.get("/posts", response_model = List[Post])
def get_posts(db: Session = Depends(get_db)):

    # implementing SQL through SQLAlchemy ORMs
    posts = db.query(models.Post).all()

    # while printing, it prints the object [<app.models.Post object at 0x000001D5D7537200>, <app.models.Post object at 0x000001D5D....]
    # but while returning posts, proper data is displayed in Postman
    print(posts)
    return posts


@app.post("/create_post", status_code = status.HTTP_201_CREATED, response_model = Post)
def create_post(payLoad: PostCreate, db: Session = Depends(get_db)):

    # implementing code through SQLAlchemy ORMs
    # new_post = models.Post(title = payLoad.title, content = payLoad.content, 
    #                        is_published = payLoad.is_published, rating = payLoad.rating)

    # A better way to create new_post by dict unpacking
    new_post = models.Post(**payLoad.model_dump())

    # commmit equivalent of SQL:
    db.add(new_post)
    db.commit()

    # refresh() to immediately get an up-to-date version of the object
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model = Post)
def get_post_by_id(id : int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f'Post with id: {id} not found')
    # it prints the object, not the data
    print(post)
    return post


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id : int, db: Session = Depends(get_db)):

    post_to_del = db.query(models.Post).filter(models.Post.id == id)

    if post_to_del.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist')
    
    post_to_del.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model = Post)
def update_post_by_id(id: int, payLoad: PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist. Unable to update!')
    
    post_query.update(payLoad.model_dump())
    db.commit()
    return post_query.first()


#                                                                        #
# ------------------------------ USER -----------------------------------#
#                                                                        #

# USER REGISTRATION
@app.post("/users", status_code = status.HTTP_201_CREATED, response_model = UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())

    # hash the password
    password_hash = hash(new_user.password)
    new_user.password = password_hash

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except IntegrityError as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Email already exists.")
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Unexpected error.')


    return new_user