from aiohttp import ClientSession, TCPConnector
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Resource, Factory, List
from fastapi import FastAPI

from app.context.controller import Controller
from app.context.checker.puppet_theatre_checker import PuppetTheatreChecker
from app.system.config import HEADERS, ENVIRONMENT, get_settings

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


async def _setup_boy():
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)


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
