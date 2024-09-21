from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise
from loguru import logger

from app.config import settings


# Настройки поключения ORM
DB_TORTOISE = dict(
    connections=dict(
        default=settings.DB_URL_SQLITE,
        ),
    apps=dict(
        models=dict(
            models=['app.config.db.models'],
            default_connection='default',
        ),
    ),
)


async def init_db(app: FastAPI):
    """Инициализация базы данных

    Args:
        app (FastAPI): Указатель на FastAPI проект
    """
    logger.info('Инициализация базы данных...')
    async with RegisterTortoise(
        app=app,
        config=DB_TORTOISE,
        generate_schemas=False,
        add_exception_handlers=False,
    ):
        logger.info('Инциализация была успешна произведена')
        yield
    logger.info('Закрытие базы данных')
    await Tortoise.close_connections()
