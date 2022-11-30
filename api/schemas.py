import datetime
from typing import Optional

from pydantic import BaseModel


class SearchParameters(BaseModel):
    region: Optional[str]
    county: Optional[str]
    area: Optional[str]
    places: Optional[str]

    class Config:
        orm_mode = True


class ResponseOut(BaseModel):
    date: Optional[datetime.datetime]
    region: Optional[str]
    county: Optional[str]
    area: Optional[list[str]]
    time: Optional[str]

    class Config:
        orm_mode = True


class ResponseOutWithStats(BaseModel):
    count: int
    search_parameters: Optional[SearchParameters]
    response: list[ResponseOut]

    class Config:
        orm_mode = True
