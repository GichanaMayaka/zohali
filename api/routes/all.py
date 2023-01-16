from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..models import MaintenanceSchedule
from ..utils import match_criteria

router = APIRouter(tags=["All Scheduled Maintenance"])


@router.get("/all", status_code=status.HTTP_200_OK, response_model=schemas.ResponseOutWithStats,
            response_model_exclude_none=True)
def get_all_scheduled_maintenance(
        db: Session = Depends(get_db),
        count: Optional[int] = Query(default=10, gt=0),
        region: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
        area: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
        place: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
        county: Optional[str] = Query(default=None, regex=r"[a-zA-Z]")
):
    response = db.query(MaintenanceSchedule).order_by(
        MaintenanceSchedule.date.desc()
    )

    response, retrieved_count = match_criteria(
        count=count, region=region, area=area, place=place, county=county, response=response, db_session=db
    )

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracked maintenance yet"
        )

    return schemas.ResponseOutWithStats(
        count=retrieved_count,
        search_parameters=schemas.SearchParameters(region=region, county=county, area=area, places=place),
        response=response
    )
