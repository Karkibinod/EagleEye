# eagle_eye_api/services/event_service.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from ..models.event import Event
from ..models.user import User
from ..models.location import Location
import uuid


def get_upcoming_events(db: Session, lookahead_days: int = 7) -> list[Event]:
    """Fetches events scheduled within the next specified number of days."""
    now = datetime.utcnow()
    future_date = now + timedelta(days=lookahead_days)
    events = db.query(Event).filter(
        Event.start_time >= now,
        Event.start_time <= future_date
    ).order_by(Event.start_time).all()
    return events


def search_events(db: Session, query: str) -> list[Event]:
    """Searches for events based on title or location."""
    search_pattern = f"%{query.lower()}%"
    events = db.query(Event).join(Location).filter(
        or_(
            Event.title.ilike(search_pattern),
            Location.name.ilike(search_pattern)
        )
    ).all()
    return events


def create_event(db: Session, title: str, start_time: datetime, end_time: datetime, location_id: int, organizer: User) -> Event:
    """Creates a new event record."""
    db_event = Event(
        title=title,
        start_time=start_time,
        end_time=end_time,
        location_id=location_id,
        organizer_id=organizer.id,
        event_id=f"EVT-{int(datetime.now().timestamp())}"
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
