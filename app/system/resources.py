from aiohttp import ClientSession, TCPConnector
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Resource, Factory, List
from fastapi import FastAPI

from app.context.controller import Controller
from app.context.checker.puppet_theatre_checker import PuppetTheatreChecker
from app.system.config import HEADERS


async def _setup_http_client():
    client = ClientSession(
        connector=TCPConnector(
            verify_ssl=False,  # TODO: research needed
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
        )
    )


async def startup_event(app: FastAPI):
    await app.container.init_resources()


async def shutdown_event(app: FastAPI):
    await app.container.shutdown_resources()
