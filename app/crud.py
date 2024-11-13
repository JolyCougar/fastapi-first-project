from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from .models import Post
from .shemas import PostCreate

class PostCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post: PostCreate):
        db_post = Post(**post.dict())
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

    def get_post(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_posts(self, skip: int = 0, limit: int = 10):
        return self.db.query(Post).offset(skip).limit(limit).all()

    def delete_post(self, post_id: int):
        post = self.get_post(post_id)
        if post is None:
            raise NoResultFound("Post not found")
        self.db.delete(post)
        self.db.commit()
        return post
