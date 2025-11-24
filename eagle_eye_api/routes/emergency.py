# eagle_eye_api/routes/emergency.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..services import emergency_service
from ..db.session import get_db
from ..models.emergency import AlertType
from ..models.user import User
from .schemas import SafetyShareRequest, SafetyShareResponse, AlertBroadcastRequest

emergency_router = Blueprint(
    'emergency', __name__, url_prefix='/api/v1/safety')


def get_db_session():
    return next(get_db())


@emergency_router.route('/share/start', methods=['POST'])
def start_share_trip():
    try:
        share_data = SafetyShareRequest(**request.json)
        db: Session = get_db_session()
        user = db.query(User).filter(User.id == 1).first()

        if not user:
            return jsonify({"error": "User authentication failed."}), 401

        new_share = emergency_service.start_safety_share(
            db,
            user=user,
            route_id=share_data.route_id,
            contact_info=share_data.contact_info
        )

        response_data = SafetyShareResponse(
            **new_share.__dict__)  # Simple dict conversion
        return jsonify(response_data.dict()), 201

    except Exception as e:
        return jsonify({"error": f"Failed to start safety share: {e}"}), 400


@emergency_router.route('/share/stop/<string:token>', methods=['POST'])
def stop_share_trip(token: str):
    try:
        db: Session = get_db_session()
        success = emergency_service.stop_safety_share(db, share_token=token)

        if success:
            return jsonify({"message": "Safety share stopped successfully."}), 200
        else:
            return jsonify({"error": "Active share session not found or already stopped."}), 404

    except Exception as e:
        return jsonify({"error": f"Failed to stop safety share: {e}"}), 500


@emergency_router.route('/alert/broadcast', methods=['POST'])
def broadcast_alert_api():
    try:
        alert_data = AlertBroadcastRequest(**request.json)
        db: Session = get_db_session()

        try:
            alert_type_enum = AlertType(alert_data.alert_type.upper())
        except ValueError:
            return jsonify({"error": f"Invalid alert type: {alert_data.alert_type}"}), 400

        new_alert = emergency_service.broadcast_alert(
            db,
            alert_type=alert_type_enum,
            location_id=alert_data.location_id,
            safe_zone_name=alert_data.safe_zone_name
        )

        return jsonify({"message": "Emergency alert broadcast successfully.", "alert_id": new_alert.alert_id}), 201

    except Exception as e:
        return jsonify({"error": f"Failed to broadcast alert: {e}"}), 500
