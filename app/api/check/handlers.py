from app.api.check.models import CheckRequest, CheckResponse
from app.context.controller import Controller
from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from app.system.resources import Container


@inject
async def check_tickets(
    req: CheckRequest,
    controller: Controller = Depends(Provide[Container.controller])
) -> CheckResponse:
    return await controller.check_tickets_availability(req)
