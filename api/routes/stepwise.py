from typing import Optional

import pendulum
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import match_criteria

router = APIRouter(tags=["Stepwise Queries"])


@router.get("/next", status_code=status.HTTP_200_OK, response_model=schemas.ResponseOutWithStats,
            response_model_exclude_none=True)
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
        models.MaintenanceSchedule.date > pendulum.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    )

    next, retrieved_count = match_criteria(
        count=count, region=region, area=area, place=place, county=county, response=next, db_session=db
    )

    if not next:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scheduled maintenance after now. Please check in later."
        )

    return schemas.ResponseOutWithStats(
        count=retrieved_count,
        search_parameters=schemas.SearchParameters(region=region, county=county, area=area, places=place),
        response=next
    )


@router.get("/prev", status_code=status.HTTP_200_OK, response_model=schemas.ResponseOutWithStats,
            response_model_exclude_none=True)
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
        models.MaintenanceSchedule.date < pendulum.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    )

    prev, retrieved_count = match_criteria(
        count=count, region=region, area=area, place=place, county=county, response=prev, db_session=db
    )

    if not prev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracked expired scheduled maintenance."
        )

    return schemas.ResponseOutWithStats(
        count=retrieved_count,
        search_parameters=schemas.SearchParameters(region=region, county=county, area=area, places=place),
        response=prev
    )


@router.get("/now", status_code=status.HTTP_200_OK, response_model=schemas.ResponseOutWithStats,
            response_model_exclude_none=True)
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
        models.MaintenanceSchedule.date == pendulum.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    )

    current, retrieved_count = match_criteria(
        count=count, region=region, area=area, place=place, county=county, response=current, db_session=db
    )

    if not current:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scheduled maintenance underway."
        )

    return schemas.ResponseOutWithStats(
        count=retrieved_count,
        search_parameters=schemas.SearchParameters(region=region, county=county, area=area, places=place),
        response=current
    )
