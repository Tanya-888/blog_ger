from db import Session
from model.models import BlogItem

class BaseController:
    @staticmethod
    def index(page=1, per_page=2):
        with Session as session:
            has_next = session.query(BlogItem).count() > page * per_page
            blog_items = session.query(BlogItem).limit(per_page).offset((page - 1) * per_page).all()

        return blog_items, has_next