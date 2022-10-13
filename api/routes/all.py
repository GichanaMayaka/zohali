from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import schemas, utils
from ..database import get_db
from ..models import MaintenanceSchedule

router = APIRouter(prefix="/all", tags=["All Scheduled Maintenance"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.ResponseOutWithStats, response_model_exclude_none=True)
def get_all_scheduled_maintenance(
    db: Session = Depends(get_db),
    count: Optional[int] = Query(default=100, gt=0),
    region: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    area: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    place: Optional[str] = Query(default=None, regex=r"[a-zA-Z]"),
    county: Optional[str] = Query(default=None, regex=r"[a-zA-Z]")
):
    response = db.query(MaintenanceSchedule).order_by(
        MaintenanceSchedule.date.desc()
    )

    response, returned_count = utils.match_criteria(
        count=count, region=region, area=area, place=place, county=county, response=response, db_session=db
    )

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracked maintenance yet"
        )

    return {
        "count": returned_count,
        "region": region,
        "county": county,
        "response": response
    }
