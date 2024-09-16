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

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    # implementing SQL through SQLAlchemy ORMs
    posts = db.query(models.Post).all()
    print(posts)
    return {"posts_data" : posts}


@app.post("/create_post", status_code = status.HTTP_201_CREATED)
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

    return {"data" : new_post}


@app.get("/posts/{id}")
def get_post_by_id(id : int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f'Post with id: {id} not found')
    # it prints the object, not the data
    print(post)
    return {"post_data" : post}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id : int, db: Session = Depends(get_db)):

    post_to_del = db.query(models.Post).filter(models.Post.id == id)

    if post_to_del.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist')
    
    post_to_del.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post_by_id(id: int, payLoad: PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist. Unable to update!')
    
    post_query.update(payLoad.model_dump())
    db.commit()
    return {'message' : post_query.first()}
