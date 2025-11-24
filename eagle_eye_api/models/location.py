# eagle_eye_api/models/location.py
from sqlalchemy import Column, Integer, String, Enum as SqlAlchemyEnum
from geoalchemy2 import Geometry
import enum
from ..db.session import Base


class LocationType(enum.Enum):
    CLASSROOM = "Classroom"
    OFFICE = "Office"
    RESTROOM = "Restroom"
    CAFETERIA = "Cafeteria"
    EVENT = "Event"
    SERVICE = "Service"
    OTHER = "Other"


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    building_name = Column(String, index=True, nullable=False)
    floor = Column(String, nullable=True)
    type = Column(SqlAlchemyEnum(LocationType),
                  default=LocationType.OTHER, nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
