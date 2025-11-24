# eagle_eye_api/models/emergency.py
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlAlchemyEnum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from ..db.session import Base


class AlertType(enum.Enum):
    SECURITY = "Security"
    MEDICAL = "Medical"
    WEATHER = "Weather"
    FIRE = "Fire"
    OTHER = "Other"


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True, nullable=False)
    type = Column(SqlAlchemyEnum(AlertType), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location = relationship("Location")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    safe_zone_name = Column(String, nullable=True)


class SafetyShare(Base):
    __tablename__ = "safety_shares"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)
    route = relationship("Route")
    contact_info = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    share_token = Column(String, unique=True, nullable=False)
