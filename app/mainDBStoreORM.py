from fastapi import FastAPI
from . import models
from .database import engine
from .routers import like, post, user, auth

# this line actually creates the tables through SQLAlchemy
# models.Base.metadata.create_all(bind = engine)
# Since table creation has been implemented to Alembic,using create_all in the code becomes redundant. 
# Alembic will handle the generation and application of SQL schema changes when migrations are executed, 
# based on versioned migration scripts. If create_all is kept in the code, it might create the tables 
# before Alembic runs, rendering the first migration unnecessary, 
# But anyways commenting it out!


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

