from databases import Database
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from .models import Post
from .shemas import PostCreate

class PostCRUD:
    def __init__(self, db: Database):
        self.db = db

    async def create_post(self, post: PostCreate):
        query = Post.__table__.insert().values(**post.dict())
        post_id = await self.db.execute(query)
        return {**post.dict(), "id": post_id}

    async def get_post(self, post_id: int):
        query = Post.__table__.select().where(Post.id == post_id)
        return await self.db.fetch_one(query)

    async def get_posts(self, skip: int = 0, limit: int = 10):
        query = Post.__table__.select().offset(skip).limit(limit)
        return await self.db.fetch_all(query)

    async def delete_post(self, post_id: int):
        query = Post.__table__.select().where(Post.id == post_id)
        post = await self.db.fetch_one(query)
        if post is None:
            raise NoResultFound("Post not found")
        delete_query = Post.__table__.delete().where(Post.id == post_id)
        await self.db.execute(delete_query)
        return post
