from app.checker.models import CheckRequest
from aiohttp import ClientSession


class Controller:

    def __init__(self, session: ClientSession):
        self._session = session

    async def check_tickets(self, req: CheckRequest):
        resp = await self._session.get(req.page)
