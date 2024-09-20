from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# format is "postgresql://user:password@postgresserver/dbname" 
SQLALCHEMY_DB_URL = 'postgresql://admin:admin@localhost/postsDB'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) 

Base = declarative_base()


# SQLAlchemy just creates tables, it cannot modify them, so if  a table is already created, and
# we modify an attribute property, it will not take effect.We will have to delete the table and then re-create it.
# It just checks if the table is present, if not create it, if present, do nothing.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()