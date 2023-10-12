from app.api.check.models import CheckRequest
from aiohttp import ClientSession, ClientResponse


class Controller:

    def __init__(self, session: ClientSession):
        self._session = session

    async def check_tickets(self, req: CheckRequest):
        resp = await self._make_request(req.page)

    async def _make_request(self, url: str, method: str = 'GET') -> ClientResponse:
        return await self._session.get(url)
