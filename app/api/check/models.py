from pydantic import BaseModel, HttpUrl


class CheckRequest(BaseModel):
    page: HttpUrl
