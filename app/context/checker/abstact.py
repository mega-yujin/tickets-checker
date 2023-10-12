from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Union

from aiohttp import ClientSession, ClientResponse, hdrs
from pydantic import BaseModel, Field
from pydantic.networks import Url


class CheckResult(BaseModel):
    tickets_available: bool
    info: Any


class PlayInfo(BaseModel):
    date: datetime
    date_id: str


class PlayInfoWithTickets(PlayInfo):
    available_tickets: Any


class Schedule(BaseModel):
    plays: list[PlayInfo] = Field(default=[])


class ScheduleWithTickets(BaseModel):
    plays: list[PlayInfoWithTickets] = Field(default=[])


class TicketsChecker(ABC):
    host: str = None

    def __init__(self, session: ClientSession):
        self._session = session

    async def _make_request(self, method: str, url: Url, data: dict = None) -> ClientResponse:
        return await self._session.request(method, url.unicode_string(), data=data)

    async def check(self, url: Url) -> CheckResult:
        schedule_page_response = await self._make_request(hdrs.METH_GET, url)
        schedule_page = await schedule_page_response.text()
        schedule = self.parse_page(schedule_page)
        available_tickets = self.get_available_ticket(schedule)
        return self.analyze_result(available_tickets)

    @abstractmethod
    def parse_page(self, page: str) -> Schedule:
        pass

    @abstractmethod
    def get_available_ticket(self, schedule: Schedule) -> ScheduleWithTickets:
        pass

    @abstractmethod
    def analyze_result(self, schedule: ScheduleWithTickets) -> CheckResult:
        pass
