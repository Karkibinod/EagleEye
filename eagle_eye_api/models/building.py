from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from ..db.session import Base


class Building(Base):
    """
    Database Model for storing UNT campus building information (Boundaries/Polygons).
    """
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)

    # Core Identifiers and Attributes (SRS: Building ID, Building Name) [cite: 139]
    building_id = Column(String, unique=True, index=True, nullable=False)
    building_name = Column(String, index=True, nullable=False)

    # Reference to floor plans/maps (SRS: Floor Plans) [cite: 139]
    floor_plans_ref = Column(String, nullable=True)

    # Geospatial Data
    # Stores the building footprint or boundary using PostGIS POLYGON.
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)

    def __repr__(self):
        return f"<Building(id={self.id}, name='{self.building_name}')>"
