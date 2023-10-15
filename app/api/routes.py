from fastapi import FastAPI, APIRouter

from app.api.check.handlers import check_tickets
from app.api.check.models import CheckResponse


def setup_routes(app: FastAPI):
    check_router = APIRouter(prefix='/check', tags=['Check'])
    check_router.api_route(path='', methods=['POST'], response_model=CheckResponse)(check_tickets)

    events_router = APIRouter(prefix='/events', tags=['Events'])

    app.include_router(check_router)
    app.include_router(events_router)
