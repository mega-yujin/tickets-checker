from fastapi import FastAPI, APIRouter
from app.checker.handlers import check_tickets


def setup_routes(app: FastAPI):
    check_router = APIRouter(prefix='/check', tags=['Check'])
    check_router.api_route(path='', methods=['POST'])(check_tickets)

    app.include_router(check_router)
