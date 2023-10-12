from aiohttp import ClientSession, ClientResponse, hdrs

from app.api.check.models import CheckRequest
from app.context.checker.abstact import TicketsChecker, CheckResult
from typing import Union


class Controller:

    def __init__(self, checkers: tuple[TicketsChecker, ...]):
        self._checkers = checkers

    async def check_tickets_availability(self, req: CheckRequest):
        checker = self.select_checker(req.page.host)
        check_result = await checker.check(req.page)
        self.process_result(check_result)

    def select_checker(self, host: str) -> Union[TicketsChecker, None]:
        return next(
            (checker for checker in self._checkers if checker.host == host),
            None
        )

    def process_result(self, check_result: CheckResult):
        pass
