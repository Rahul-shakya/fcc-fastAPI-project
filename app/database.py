from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# format is "postgresql://user:password@postgresserver/db" 
SQLALCHEMY_DB_URL = 'postgresql://admin:admin@localhost/postsDB'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) 

Base = declarative_base()