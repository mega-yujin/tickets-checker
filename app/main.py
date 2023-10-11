from fastapi import FastAPI
import uvicorn

from app.api.routes import setup_routes
from app.system.config import get_settings
from app.system.middlewares import setup_middlewares
from app.system.resources import ExternalDependencyContainer

settings = get_settings()


def prepare_app():
    app = FastAPI()
    container = ExternalDependencyContainer()
    app.container = container
    setup_routes(app)
    setup_middlewares(app)
    return app


def start_app():
    uvicorn.run(
        app=prepare_app(),
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )


if __name__ == "__main__":
    start_app()
