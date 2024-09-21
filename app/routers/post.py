#                                                                        #
# ------------------------------ POST -----------------------------------#
#                                                                        #

import string
from tokenize import String
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func

# importing error
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session 
from ..database import engine, get_db

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


# return type is a list of Posts, hence response_model is a list of posts

# search: Optional[str] = '' has a default empty string because Non-default arguments must appear 
# before default arguments in the parameter list.
@router.get("/", response_model = List[schemas.PostLike])
def get_posts(db: Session = Depends(get_db), user_data: str = Depends(oauth2.get_current_user),
              limit: int = 5, skip: int = 0, search: Optional[str] = ''):

    # implementing SQL through SQLAlchemy ORMs
    # old query
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # raw SQL query for fetching posts and the number of likes for each post:
        # -- to avoid counting null values, count(likes.user_id)
        # -- this is the final query which gives us posts and the number of likes
        # select tb_posts.*, count(likes.user_id) as likes
        # from tb_posts left join likes 
        # on tb_posts.id = likes.post_id
        # group by tb_posts.id;

    # now performing the same SQL query using SQL Alchemy
    # added filter query at the end
    posts_with_like_count = db.query(models.Post, 
                                     func.count(models.Like.post_id).label('likes')
                                     ).join(
                                         models.Like, models.Like.post_id == models.Post.id, isouter = True
                                         ).group_by(models.Post.id).filter(
                                             models.Post.title.contains(search)
                                             ).limit(limit).offset(skip).all()
    
    # tuple unpacking required, it threw an error if directly returned without the response model
    # The code works even if we return result
    # result = list(map(lambda x: x._mapping, posts_with_like_count))

    # if we want to fetch the posts of logged in user only
    # posts = db.query(models.Post).filter(models.Post.user_id == user_data.id).all()

    # while printing, it prints the object [<app.models.Post object at 0x000001D5D7537200>, <app.models.Post object at 0x000001D5D....]
    # but while returning posts, proper data is displayed in Postman
    print(posts_with_like_count)
    return posts_with_like_count

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(payLoad: schemas.PostCreate, db: Session = Depends(get_db), user_data: str = Depends(oauth2.get_current_user)):

    # implementing code through SQLAlchemy ORMs
    # new_post = models.Post(title = payLoad.title, content = payLoad.content, 
    #                        is_published = payLoad.is_published, rating = payLoad.rating)

    # type of user_data is <class 'app.schemas.TokenData'>. It contains all the details of the user
    

    curr_user_id = user_data.id
    # A better way to create new_post by dict unpacking
    # models.Post is the SQL Alchemy model
    new_post = models.Post(user_id = curr_user_id, **payLoad.model_dump())

    # commmit equivalent of SQL:
    db.add(new_post)
    db.commit()

    # refresh() to immediately get an up-to-date version of the object
    db.refresh(new_post)
    
    # testing the values 
    print(curr_user_id)   # o/p 37
    print(user_data.email)   # o/p test@gmail.com
    print(user_data)  # o/p <app.models.User object at 0x00000177742ADA90>

    return new_post


@router.get("/{id}", response_model = schemas.PostLike)
def get_post_by_id(id : int, db: Session = Depends(get_db), user_data: str = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post_with_like_count = db.query(models.Post, 
                                     func.count(models.Like.post_id).label('likes')
                                     ).join(
                                         models.Like, models.Like.post_id == models.Post.id, isouter = True
                                         ).group_by(models.Post.id).filter(
                                             models.Post.id == id).first()
    if not post_with_like_count:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f'Post with id: {id} not found')
    
    # if we want the funtionality of: only fetch post owned by the logged in user
    # if post.user_id != user_data.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform this action')
    
    # it prints the object, not the data
    print(post_with_like_count)
    return post_with_like_count


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id : int, db: Session = Depends(get_db), user_data: str = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_del = post_query.first()

    if post_to_del is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist')
    
    # only delete posts owned by the logged in user
    if post_to_del.user_id != user_data.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform this action')

    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = schemas.Post)
def update_post_by_id(id: int, payLoad: schemas.PostCreate, db: Session = Depends(get_db), user_data: str = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} does not exist. Unable to update!')
    
    # only update posts owned by the logged in user
    if post_to_update.user_id != user_data.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform this action')
    
    post_query.update(payLoad.model_dump())
    db.commit()
    return post_query.first()