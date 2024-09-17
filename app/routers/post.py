#                                                                        #
# ------------------------------ POST -----------------------------------#
#                                                                        #
# 

from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List

# importing error
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session 
from ..database import engine, get_db

router = APIRouter()


# return type is a list of Posts, hence response_model is a list of posts
@router.get("/posts", response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    # implementing SQL through SQLAlchemy ORMs
    posts = db.query(models.Post).all()

    # while printing, it prints the object [<app.models.Post object at 0x000001D5D7537200>, <app.models.Post object at 0x000001D5D....]
    # but while returning posts, proper data is displayed in Postman
    print(posts)
    return posts


@router.post("/create_post", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(payLoad: schemas.PostCreate, db: Session = Depends(get_db)):

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


@router.get("/posts/{id}", response_model = schemas.Post)
def get_post_by_id(id : int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f'Post with id: {id} not found')
    # it prints the object, not the data
    print(post)
    return post


@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id : int, db: Session = Depends(get_db)):

    post_to_del = db.query(models.Post).filter(models.Post.id == id)

    if post_to_del.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist')
    
    post_to_del.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model = schemas.Post)
def update_post_by_id(id: int, payLoad: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist. Unable to update!')
    
    post_query.update(payLoad.model_dump())
    db.commit()
    return post_query.first()