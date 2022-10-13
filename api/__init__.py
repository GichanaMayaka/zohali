from enum import Enum
from typing import Dict, Optional, Union

from fastapi import Body, Cookie, Depends, FastAPI, Path, Query, status
from numpy import place
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import get_db
from .models import MaintenanceSchedule
from .routes import all, stepwise
from . import schemas


app = FastAPI()

app.include_router(all.router)
app.include_router(stepwise.router)


@app.get("/{name}", status_code=status.HTTP_200_OK, response_model=list[schemas.ResponseOut], response_model_exclude_none=True, tags=["Index"])
async def index(
    name: str = Path(default=None, regex=r"[a-zA-Z]", min_length=1),
    db: Session = Depends(get_db)
):
    response = db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.places.ilike(f"%{name}%")
    ).order_by(
        MaintenanceSchedule.date.desc()
    ).all()

    return response
