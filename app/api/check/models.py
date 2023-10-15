from typing import Union

from pydantic import BaseModel, HttpUrl

from app.context.checker.abstact import TicketsInfo


class CheckRequest(BaseModel):
    page: HttpUrl
    notify: Union[tuple[str], None] = None
    negative_response: bool = False


class CheckResponse(BaseModel):
    show_title: str
    result: bool
    details: Union[tuple[TicketsInfo], None] = None
