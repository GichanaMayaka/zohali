import datetime
from typing import Optional

from pydantic import BaseModel


class ResponseOut(BaseModel):
    date: Optional[datetime.datetime]
    region: Optional[str]
    county: Optional[str]
    area: Optional[list[str]]
    places: Optional[list[str]]
    time: Optional[str]

    class Config:
        orm_mode = True


class ResponseOutWithStats(BaseModel):
    count: int
    region: Optional[str]
    county: Optional[str]
    response: list[ResponseOut]

    class Config:
        orm_mode = True
