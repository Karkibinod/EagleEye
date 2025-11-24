# eagle_eye_api/services/emergency_service.py
from sqlalchemy.orm import Session
from ..models.emergency import EmergencyAlert, AlertType, SafetyShare
from ..models.user import User
from .routing_service import get_indoor_campus_route
import uuid
from datetime import datetime


def broadcast_alert(db: Session, alert_type: AlertType, location_id: int or None, safe_zone_name: str or None) -> EmergencyAlert:
    """Creates and saves a new emergency alert."""
    db_alert = EmergencyAlert(
        alert_id=str(uuid.uuid4()),
        type=alert_type,
        location_id=location_id,
        safe_zone_name=safe_zone_name
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def start_safety_share(db: Session, user: User, route_id: int, contact_info: str) -> SafetyShare:
    """Initiates a live location sharing session."""
    db_share = SafetyShare(
        user_id=user.id,
        route_id=route_id,
        contact_info=contact_info,
        share_token=str(uuid.uuid4())
    )
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


def get_safe_route(db: Session, current_location_id: int, alert: EmergencyAlert) -> list:
    """Calculates the fastest route to the nearest safe zone during an active alert."""
    # Placeholder: Assuming the safe zone is defined by a specific Location ID (e.g., 500)
    nearest_safe_zone_id = 500
    safe_route = get_indoor_campus_route(
        db, current_location_id, nearest_safe_zone_id, accessible_only=False)
    return safe_route


def stop_safety_share(db: Session, share_token: str) -> bool:
    """Stops an active safety sharing session."""
    share = db.query(SafetyShare).filter(
        SafetyShare.share_token == share_token).first()
    if share and share.is_active:
        share.is_active = False
        db.commit()
        return True
    return False
