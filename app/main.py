from fastapi import FastAPI
from contextlib import asynccontextmanager
from tortoise import Tortoise

from .time_filter import router
from app.config.db.setup import init_db


init_db = asynccontextmanager(init_db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with init_db(app):
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
