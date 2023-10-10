from pydantic import BaseModel


class CheckRequest(BaseModel):
    page: str
