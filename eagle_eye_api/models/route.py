# eagle_eye_api/models/route.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from geoalchemy2 import Geometry
from ..db.session import Base


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String, unique=True, index=True, nullable=False)
    start_location_id = Column(
        Integer, ForeignKey("locations.id"), nullable=False)
    end_location_id = Column(Integer, ForeignKey(
        "locations.id"), nullable=False)
    path_geom = Column(
        Geometry(geometry_type='LINESTRING', srid=4326), nullable=False)
    is_accessible = Column(Boolean, default=False, nullable=False)
    weight_distance_m = Column(Integer, nullable=False)
