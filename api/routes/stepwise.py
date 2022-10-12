import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(tags=["Stepwise Queries"])


@router.get("/next", status_code=status.HTTP_200_OK, response_model=list[schemas.ResponseOut], response_model_exclude_none=True)
def get_next_scheduled_maintenance(
    db: Session = Depends(get_db),
    count: Optional[int] = Query(default=5, gt=0),
    region: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    area: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    place: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    county: Optional[str] = Query(default=None, regex=r"[a-zA-Z]")
):

    next = db.query(
        models.MaintenanceSchedule
    ).filter(
        models.MaintenanceSchedule.date > dt.datetime.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    )

    next = utils.Utilities.match_criteria(
        count, region, area, place, county, response=next
    )

    if not next:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scheduled maintenance after now. Please check in later."
        )

    return {
        "count": count,
        "response": next
    }


@router.get("/prev", status_code=status.HTTP_200_OK, response_model=schemas.ResponseOutWithStats, response_model_exclude_none=True)
def get_prev_scheduled_maintenance(
    db: Session = Depends(get_db),
    count: Optional[int] = Query(default=5, gt=0),
    region: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    area: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    place: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    county: Optional[str] = Query(default=None, regex=r"[a-zA-Z]")
):

    prev = db.query(
        models.MaintenanceSchedule
    ).filter(
        models.MaintenanceSchedule.date < dt.datetime.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    )

    prev = utils.Utilities.match_criteria(
        count=count, region=region, area=area, place=place, county=county, response=prev
    )

    if not prev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracked expired scheduled maitenance."
        )

    return {
        "count": count,
        "response": prev
    }


@router.get("/now", status_code=status.HTTP_200_OK, response_model=list[schemas.ResponseOut], response_model_exclude_none=True)
def get_current_maintenance(
    db: Session = Depends(get_db),
    count: Optional[int] = Query(default=5, gt=0),
    region: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    area: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    place: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    county: Optional[str] = Query(default=None, regex=r"[a-zA-Z]")
):
    current = db.query(
        models.MaintenanceSchedule
    ).filter(
        models.MaintenanceSchedule.date == dt.datetime.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    )

    current = utils.Utilities.match_criteria(
        count=count, region=region, area=area, place=place, county=county, response=current
    )

    if not current:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scheduled maintenance underway."
        )

    return {
        "count": count,
        "response": current
    }
