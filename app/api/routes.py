from fastapi import FastAPI, APIRouter
from app.api.check.handlers import check_tickets


def setup_routes(app: FastAPI):
    check_router = APIRouter(prefix='/check', tags=['Check'])
    check_router.api_route(path='', methods=['POST'])(check_tickets)

    events_router = APIRouter(prefix='/events', tags=['Events'])

    app.include_router(check_router)
    app.include_router(events_router)
