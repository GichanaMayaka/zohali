from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP


class MaintenanceSchedule(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    region = Column(String, nullable=True)
    area = Column(String, nullable=True)
    places = Column(String, nullable=True)
    time = Column(String, nullable=True)
    date = Column(TIMESTAMP(timezone=True), nullable=True)
    county = Column(String, nullable=True)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    file_path = Column(String, nullable=True)

    __tablename__ = "maintenance_schedule"
