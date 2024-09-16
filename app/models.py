from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# this is the SQL Alchemy model

class Post(Base):
    __tablename__ = 'tb_posts'

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    is_published = Column(Boolean, server_default = 'False', nullable = False)
    rating = Column(Integer, nullable = True)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))