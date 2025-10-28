from sqlalchemy import Column, Integer, String, DateTime
from model.base import Base

class BlogItem(Base):
    __tablename__ = 'blog_items'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
