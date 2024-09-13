from typing import Optional
from fastapi import FastAPI
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