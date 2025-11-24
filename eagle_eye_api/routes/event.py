# eagle_eye_api/routes/event.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..services import event_service
from ..db.session import get_db
from ..models.user import User  # Assuming User for organizer lookups
from .schemas import EventCreate, EventResponse

event_router = Blueprint('event', __name__, url_prefix='/api/v1/events')


def get_db_session():
    return next(get_db())


@event_router.route('/', methods=['GET'])
def get_events():
    try:
        db: Session = get_db_session()
        lookahead_days = request.args.get('days', 7, type=int)
        events = event_service.get_upcoming_events(
            db, lookahead_days=lookahead_days)
        return jsonify([EventResponse.from_orm(e).dict() for e in events]), 200

    except Exception as e:
        return jsonify({"error": f"Failed to retrieve events: {e}"}), 500


@event_router.route('/search', methods=['GET'])
def search_events_api():
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({"error": "Query parameter 'q' is required for search."}), 400

        db: Session = get_db_session()
        events = event_service.search_events(db, query=query)
        return jsonify([EventResponse.from_orm(e).dict() for e in events]), 200

    except Exception as e:
        return jsonify({"error": f"Event search failed: {e}"}), 500


@event_router.route('/', methods=['POST'])
def create_event_api():
    try:
        event_data = EventCreate(**request.json)
        db: Session = get_db_session()

        # MOCK USER: Replace with actual token parsing and user lookup
        organizer = db.query(User).filter(User.id == 1).first()

        if not organizer:
            return jsonify({"error": "Organizer authentication failed."}), 401

        new_event = event_service.create_event(
            db,
            title=event_data.title,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            location_id=event_data.location_id,
            organizer=organizer
        )

        return jsonify(EventResponse.from_orm(new_event).dict()), 201

    except Exception as e:
        return jsonify({"error": f"Event creation failed: {e}"}), 400
