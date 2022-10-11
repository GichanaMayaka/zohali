import datetime
from typing import Optional

from pydantic import BaseModel


class AllResponse(BaseModel):
    id: Optional[str]
    region: Optional[str]
    area: Optional[str]
    places: Optional[str]
    time: Optional[str]
    date: Optional[datetime.datetime]
    county: Optional[str]

    class Config:
        orm_mode = True
