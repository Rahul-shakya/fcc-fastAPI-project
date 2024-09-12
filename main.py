from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "This is a drill."}

@app.get("/test_get")
async def root():
    return {"message" : "This is a test."}

@app.post("/create_post")
def create_post(payLoad: Post):

    # this is how we extract the data from body of the payload 
    # return {"title" : f"title is {payLoad['title']}", "content": f"Content is {payLoad['content']}"}

    # using pydantic, simple printing does the job, we dont have to do like before |
    print(payLoad)
    print(f"{payLoad.title}  {payLoad.content}")
    return True