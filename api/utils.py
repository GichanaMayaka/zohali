from typing import Any, Optional

import pandas as pd

from .models import MaintenanceSchedule


def match_criteria(
    count: Optional[int],
    region: Optional[str],
    area: Optional[str],
    place: Optional[str],
    county: Optional[str],
    db_session,
    response: Any
    ) -> tuple[list[dict[Any, Any]], int]:
    """
        Matches the various query parameters in the db session query object returning the specified response with the limit.
        Returns a tuple of the response model as a dictionary and the retrieved count as an int
    """
    if region:
        response = response.filter(
            MaintenanceSchedule.region.ilike(f"%{region}%")
        )

    if area:
        response = response.filter(
            MaintenanceSchedule.area.ilike(f"%{area}%")
        )

    if place:
        response = response.filter(
            MaintenanceSchedule.places.ilike(f"%{place}%")
        )

    if county:
        response = response.filter(
            MaintenanceSchedule.county.ilike(f"%{county}%")
        )

    dataframe = pd.read_sql(response.limit(
        limit=count
    ).statement, db_session.bind
    )

    dataframe.places = dataframe.places.str.split(",")
    dataframe.area = dataframe.area.str.split(",")

    return dataframe.to_dict(orient="records"), dataframe.shape[0]
