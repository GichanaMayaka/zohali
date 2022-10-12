import datetime
from typing import Optional

from pydantic import BaseModel


class ResponseOut(BaseModel):
    date: Optional[datetime.datetime]
    region: Optional[str]
    county: Optional[str]
    area: Optional[str]
    places: Optional[str]
    time: Optional[str]

    class Config:
        orm_mode = True


class ResponseOutWithStats(BaseModel):
    count: int
    response: list[ResponseOut]
