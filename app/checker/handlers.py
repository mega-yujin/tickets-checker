from app.checker.models import CheckRequest
from app.checker.controller import Controller
from fastapi import Depends
from dependency_injector.wiring import Provide
from app.system.resources import ExternalDependencyContainer


def check_tickets(req: CheckRequest, controller: Controller = Depends(Provide[ExternalDependencyContainer.client_session])):
    return controller.check_tickets(req)
