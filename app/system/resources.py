from aiohttp import ClientSession, TCPConnector
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Resource, Factory, List
from fastapi import FastAPI

from app.context.controller import Controller
from app.context.checker.puppet_theatre_checker import PuppetTheatreChecker
from app.context.notifier.email_notifier import EmailNotifier, EmailNotifierConfig
from app.system.config import HEADERS, get_settings

settings = get_settings()


async def _setup_http_client():
    client = ClientSession(
        connector=TCPConnector(
            verify_ssl=False,  # TODO: research needed
            keepalive_timeout=3,
        ),
        headers=HEADERS,
    )
    yield client
    await client.close()


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=['app.api'])

    client_session = Resource(_setup_http_client)
    controller = Factory(
        Controller,
        checkers=List(
            Singleton(PuppetTheatreChecker, session=client_session)
        ),
        notifiers=List(
            Singleton(
                EmailNotifier,
                config=EmailNotifierConfig(
                    host=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    login=settings.SMTP_LOGIN,
                    password=settings.SMTP_PASSWORD,
                )
            )
        ),
    )


async def startup_event(app: FastAPI):
    await app.container.init_resources()


async def shutdown_event(app: FastAPI):
    await app.container.shutdown_resources()
