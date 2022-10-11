from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session


from ..database import get_db
from ..models import MaintenanceSchedule
from .. import schemas


router = APIRouter(prefix="/all", tags=["All Scheduled Maintenance"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.AllResponse], response_model_exclude_none=True)
def get_all(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(default=100, gt=0)
):
    response = db.query(MaintenanceSchedule).limit(limit=limit).all()

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracked maintenance yet"
        )

    return response
