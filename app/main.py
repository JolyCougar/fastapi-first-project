from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from .models import Base
from .shemas import PostShema, PostCreate
from .database import engine
from .dependencies import get_db
from .crud import PostCRUD

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/posts/", response_model=PostShema)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post_crud = PostCRUD(db)
    return post_crud.create_post(post)

@app.get("/posts/{post_id}", response_model=PostShema)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post_crud = PostCRUD(db)
    post = post_crud.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/posts/", response_model=list[PostShema])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    post_crud = PostCRUD(db)
    return post_crud.get_posts(skip=skip, limit=limit)

@app.delete("/posts/{post_id}", response_model=PostShema)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_crud = PostCRUD(db)
    try:
        return post_crud.delete_post(post_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Post not found")
