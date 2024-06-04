from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from random import choice

USER_AGENTS = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
)

HEADERS = {
    'user-agent': choice(USER_AGENTS),
}


class AppConfig(BaseSettings):
    SECRET_KEY: str
    BOT_TOKEN: str
    APP_HOST: str
    APP_PORT: int
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_LOGIN: str
    SMTP_PASSWORD: str

    model_config = SettingsConfigDict(env_file='config.env', env_file_encoding='utf-8', extra='allow')


@lru_cache()
def get_config():
    return AppConfig()
