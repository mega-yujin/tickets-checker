from aiohttp import ClientSession, TCPConnector
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Resource, Factory, List, Configuration
from fastapi import FastAPI

from app.context.controller import Controller
from app.context.checker.puppet_theatre_checker import PuppetTheatreChecker
from app.context.notifier.email_notifier import EmailNotifier, EmailNotifierConfig
from app.system.config import HEADERS


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
    config = Configuration()

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
                    host=config.SMTP_HOST,
                    port=config.SMTP_PORT,
                    login=config.SMTP_LOGIN,
                    password=config.SMTP_PASSWORD,
                )
            )
        ),
    )


async def startup_event(app: FastAPI):
    await app.container.init_resources()


async def shutdown_event(app: FastAPI):
    await app.container.shutdown_resources()
