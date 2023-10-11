from aiohttp import ClientSession
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration
from dependency_injector.providers import Container
from dependency_injector.providers import Factory, Singleton
from fastapi import FastAPI


class ExternalDependencyContainer(DeclarativeContainer):
    """Хранилище ресурсов внешних сервисов."""

    config = Configuration(strict=True)
    client_session = Singleton(ClientSession)


async def startup_event(app: FastAPI):  # noqa: WPS213
    """Инициализация ресурсов приложения."""


async def shutdown_event(app: FastAPI):
    """Закрытие ресурсов приложения."""
