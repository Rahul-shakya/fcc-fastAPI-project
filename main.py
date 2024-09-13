from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    
    # optional default values --
    isPublic: bool = False
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
        return False

app = FastAPI()

posts = DataStore()

@app.get("/")
async def get_posts():
    return {"posts_data" : posts.return_posts()}


@app.post("/create_post")
def create_post(payLoad: Post):

    # this is how we extract the data from body of the payload 
    # return {"title" : f"title is {payLoad['title']}", "content": f"Content is {payLoad['content']}"}

    # using pydantic, simple printing does the job, we dont have to do like before
    payload_dict = payLoad.model_dump()
    payload_dict['id'] = posts.curr_length()
    # print(f"{payLoad.title}  {payLoad.content} {payLoad.isPublic} {payLoad.rating}")

    posts.add_post(payload_dict)
    print(f"Added : {payload_dict}")

    return True


@app.get("/posts/{id}")
def get_post_by_id(id : int, response: Response):
    post = posts.find_post_by_id(id)
    print(post)
    if not post:
        # clean way:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'Post with id: {id} not found')
    
        # This is another not so clean way to do this:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f'post with id: {id} not found'}
    return {"post_detail" : post}