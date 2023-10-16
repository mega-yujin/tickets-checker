from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Union

from aiohttp import ClientSession, ClientResponse, hdrs
from pydantic import BaseModel, Field, ConfigDict
from pydantic.networks import Url


class ParseException(Exception):
    """Raises when error occurred during parse process."""

    def __init__(self, error: str):
        self.error = error
        self.message = f'Error during parse process: {self.error}'
        super().__init__(self.message)


class TicketsInfo(BaseModel):
    date: datetime
    tickets: Any = Field(default=None)  # TODO: TypeVar

    model_config = ConfigDict(extra='allow')


class Show(BaseModel):
    theater: str
    show_name: str
    schedule: list[TicketsInfo] = Field(default=[])


class CheckResult(BaseModel):
    show: Show
    tickets_available: bool = False


class CheckResultDetail(BaseModel):
    date: datetime
    available_tickets: int


class TicketsChecker(ABC):
    host: str = None

    def __init__(self, session: ClientSession):
        self._session = session

    async def _make_request(
            self,
            method: str,
            url: Union[Url, str],
            data: dict = None,
            params: dict[str, str] = None,
    ) -> ClientResponse:
        if isinstance(url, Url):
            url = url.unicode_string()

        if data:
            pass
        return await self._session.request(method, url, data=data, params=params)

    async def check(self, url: Url) -> CheckResult:
        schedule_page_response = await self._make_request(hdrs.METH_GET, url)
        schedule_page = await schedule_page_response.text()
        show_data = self.parse_page(schedule_page)
        await self.get_available_ticket(show_data.schedule)
        return self.analyze_result(show_data)

    def parse_page(self, page: str) -> Show:
        try:
            return self._parse_page(page)
        except Exception as err:
            raise ParseException(str(err))

    @abstractmethod
    def _parse_page(self, page: str) -> Show:
        pass

    @abstractmethod
    async def get_available_ticket(self, schedule: list[TicketsInfo]):
        pass

    @abstractmethod
    def analyze_result(self, show_info: Show) -> CheckResult:
        pass
