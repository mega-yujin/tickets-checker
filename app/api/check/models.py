from enum import Enum
from typing import Union

from pydantic import BaseModel, HttpUrl

from app.context.checker.abstact import TicketsInfo


class ErrorResponse(BaseModel):
    error: str


class NotificationChannelEnum(str, Enum):
    email = 'email'
    telegram = 'telegram'


class NotificationChannel(BaseModel):
    channel: NotificationChannelEnum
    receivers: tuple[str, ...]


class CheckRequest(BaseModel):
    page: HttpUrl
    notify: Union[tuple[NotificationChannel, ...], None] = None
    negative_response: bool = False


class CheckResponse(BaseModel):
    show_title: str
    result: bool
    details: Union[tuple[TicketsInfo, ...], None] = None
