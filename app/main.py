from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from .models import Base
from databases import Database
from .database import database, engine
from .shemas import PostCreate, PostResponse
from .crud import PostCRUD
from .dependencies import get_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Database = Depends(get_db)):
    post_crud = PostCRUD(db)
    return await post_crud.create_post(post)


@app.get("/posts/{post_id}", response_model=PostResponse)
async def read_post(post_id: int, db: Database = Depends(get_db)):
    post_crud = PostCRUD(db)
    post = await post_crud.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/posts/", response_model=list[PostResponse])
async def read_posts(skip: int = 0, limit: int = 10, db: Database = Depends(get_db)):
    post_crud = PostCRUD(db)
    return await post_crud.get_posts(skip=skip, limit=limit)


@app.delete("/posts/{post_id}", response_model=PostResponse)
async def delete_post(post_id: int, db: Database = Depends(get_db)):
    post_crud = PostCRUD(db)
    try:
        return await post_crud.delete_post(post_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Post not found")
