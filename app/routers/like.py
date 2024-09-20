#                                                                        #
# ------------------------------ Like -----------------------------------#
#                                                                        #

from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2, database
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session 
from ..database import get_db

router = APIRouter(
    prefix = "/like",
    tags = ['Like']
)

# post oprn because we are sending info to the server
@router.post("/", status_code = status.HTTP_201_CREATED,  response_model = None)
def like(vote: schemas.Like, db: Session = Depends(get_db), user_data: str = Depends(oauth2.get_current_user)):

    # this is also a way to check if a post we're trying to upvote exists or not 
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post does not exist!")
        

    # this query checks if the current user has already liked a post or not
    # if the user has not liked, it is an empty query, if not it returns that row
    like_query = db.query(models.Like).filter(models.Like.post_id == vote.post_id,
                                    models.Like.user_id == user_data.id)
    found_like = like_query.first()
    
    print(user_data.id)


    if(vote.direction == 1):

        # if the query returned, it means that the user is trying to like a post which they have
        # already liked
        if found_like:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                                detail = f'User {user_data.id} has already liked the post {vote.post_id} ')
        new_vote = models.Like(post_id = vote.post_id, user_id = user_data.id)

        try: 
            db.add(new_vote)
            db.commit()
        except IntegrityError as e:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="This post does not exist!")
        except Exception as e:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Unexpected error.')
        
        return {'message'  : ' User liked the post'}
    
    else:
        if not found_like:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f'You cannot unlike a post which has not been liked!')
        
        # if the user has liked the post, then unlike the post by deleting that record
        like_query.delete(synchronize_session = False)
        db.commit()

        return {'message' : 'Unliked the post!'}