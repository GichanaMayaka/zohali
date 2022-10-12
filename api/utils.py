from typing import Any, Optional

from .models import MaintenanceSchedule


class Utilities:
    @staticmethod
    def match_criteria(count: Optional[int], region: Optional[str], area: Optional[str], place: Optional[str], county: Optional[str], response: Any) -> Any:
        """Matches the various query parameters in the db session query object returning the specified response with the limit"""
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

        return response.limit(limit=count).all()
