from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float

    SQLALCHEMY_DATABASE_URL: str

    APP_HOST: str
    APP_PORT: int

    model_config = SettingsConfigDict(env_file='config.env', env_file_encoding='utf-8')


@lru_cache()
def get_settings():
    return AppSettings()
