from databases import Database
from .database import database

async def get_db():
    return database