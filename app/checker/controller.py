from app.checker.models import CheckRequest
from aiohttp import ClientSession


class Controller:

    def __init__(self, session: ClientSession):
        self._session = session

    def check_tickets(self, req: CheckRequest):
        print(f'request: {req}')
