from app.checker.models import CheckRequest
from app.checker.controller import Controller
from fastapi import Depends


def check_tickets(req: CheckRequest, controller: Controller = Depends()):
    return controller.check_tickets(req)
