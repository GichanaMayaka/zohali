from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Stepwise Queries"])


@router.get("/next", status_code=status.HTTP_200_OK, response_model=list[schemas.AllResponse], response_model_exclude_none=True)
def get_next_scheduled_maintenance(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(default=1, gt=0)
):

    next = db.query(
        models.MaintenanceSchedule
    ).filter(
        models.MaintenanceSchedule.date > datetime.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    ).limit(limit=limit).all()

    if not next:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scheduled maintenance after now. Please check in later."
        )

    return next


@router.get("/prev", status_code=status.HTTP_200_OK, response_model=list[schemas.AllResponse], response_model_exclude_none=True)
def get_prev_scheduled_maintenance(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(default=1, gt=0)
):

    prev = db.query(
        models.MaintenanceSchedule
    ).filter(
        models.MaintenanceSchedule.date < datetime.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    ).limit(limit=limit).all()

    if not prev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracked expired scheduled maitenance."
        )

    return prev


@router.get("/now", status_code=status.HTTP_200_OK, response_model=list[schemas.AllResponse], response_model_exclude_none=True)
def get_current_maintenance(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(default=1, gt=0)
):
    current = db.query(
        models.MaintenanceSchedule
    ).filter(
        models.MaintenanceSchedule.date == datetime.now()
    ).order_by(
        models.MaintenanceSchedule.date.desc()
    ).limit(limit=limit).all()

    if not current:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scheduled maintenance underway."
        )

    return current
