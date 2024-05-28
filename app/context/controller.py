from typing import Union

from pydantic import EmailStr

from app.api.check.models import CheckRequest, CheckResponse, ErrorResponse
from app.context.checker.abstact import TicketsChecker, CheckResult
from app.context.notifier.abstract import Notifier


class WrongPageException(Exception):
    """Raises when checker for requested page doesn't exist
    or wrong requested page host."""

    def __init__(self):
        self.message = "requested page doesn't exist or wrong requested page host"
        super().__init__(self.message)


class Controller:

    def __init__(self, checkers: tuple[TicketsChecker, ...], notifiers: tuple[Notifier, ...]):
        self._checkers = checkers
        self._notifiers = notifiers

    async def check_tickets_availability(self, req: CheckRequest) -> Union[CheckResponse, ErrorResponse]:
        try:
            checker = self.select_checker(req.page.host)
            check_result = await checker.check(req.page)
            response = self.process_result(check_result)
            if req.notify:
                self.send_notifications(req.notify, check_result)
            return response
        except Exception as err:
            return ErrorResponse(error=str(err))

    def select_checker(self, host: str) -> Union[TicketsChecker, None]:
        checker = next(
            (checker for checker in self._checkers if checker.host == host),
            None
        )
        if checker is None:
            raise WrongPageException
        return checker

    def process_result(self, check_result: CheckResult) -> CheckResponse:
        response = CheckResponse(
            result=check_result.tickets_available,
            show_title=check_result.show.show_name,
        )
        if check_result.tickets_available:
            response.details = check_result.show.schedule
        return response

    def send_notifications(self, receivers: tuple[str, ...], resp: CheckResult):
        pass
