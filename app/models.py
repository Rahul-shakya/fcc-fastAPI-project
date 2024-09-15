from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = 'test_posts'

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'False', nullable = False)
    rating = Column(Integer, nullable = True)
    