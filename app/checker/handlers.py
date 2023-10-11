from app.checker.models import CheckRequest
from app.checker.controller import Controller
from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from app.system.resources import ExternalDependencyContainer


@inject
async def check_tickets(
    req: CheckRequest,
    controller: Controller = Depends(Provide[ExternalDependencyContainer.controller])
):
    return await controller.check_tickets(req)
