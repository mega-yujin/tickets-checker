from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from functools import partial
import uvicorn

from app.api.routes import setup_routes
from app.system.config import get_settings
from app.system.middlewares import setup_middlewares
from app.system.resources import Container, startup_event, shutdown_event

settings = get_settings()


def prepare_bot() -> Bot:
    bot = Bot(settings.BOT_TOKEN, parse_mode="HTML")
    return bot


def prepare_app() -> FastAPI:
    app = FastAPI()
    container = Container()
    app.container = container
    setup_routes(app)
    setup_middlewares(app)

    app.on_event('startup')(partial(startup_event, app))
    app.on_event('shutdown')(partial(shutdown_event, app))
    return app


def start_app():
    uvicorn.run(
        app=prepare_app(),
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )


if __name__ == "__main__":
    start_app()
