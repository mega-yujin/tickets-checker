from aiohttp import ClientSession
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton
from fastapi import FastAPI
from app.checker.controller import Controller


class ExternalDependencyContainer(DeclarativeContainer):
    """Хранилище ресурсов внешних сервисов."""

    wiring_config = WiringConfiguration(modules=["app.checker.handlers"])

    client_session = Singleton(ClientSession)
    controller = Factory(Controller, session=client_session)


async def startup_event(app: FastAPI):  # noqa: WPS213
    """Инициализация ресурсов приложения."""


async def shutdown_event(app: FastAPI):
    """Закрытие ресурсов приложения."""
