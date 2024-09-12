from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "This is a drill."}

@app.get("/test_get")
async def root():
    return {"message" : "This is a test."}

@app.post("/create_post")
def create_post():
    return {"message" : "This is a post"}