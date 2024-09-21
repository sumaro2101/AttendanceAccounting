from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config


config = Config('.env')


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore'
    )

    DB_URL_SQLITE: str = config('DB_URL_SQLITE')

settings = Settings()
