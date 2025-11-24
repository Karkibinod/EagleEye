# eagle_eye_api/routes/navigation.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..services import routing_service
from ..db.session import get_db
from .schemas import RouteRequest, RouteResponse

navigation_router = Blueprint(
    'navigation', __name__, url_prefix='/api/v1/navigate')


def get_db_session():
    return next(get_db())


@navigation_router.route('/route', methods=['POST'])
def get_route():
    try:
        route_data = RouteRequest(**request.json)
        db: Session = get_db_session()
        start_coords = (route_data.start_lat, route_data.start_lon)

        full_route_result = routing_service.calculate_full_route(
            db=db,
            start_coords=start_coords,
            end_location_id=route_data.end_location_id,
            accessible_only=route_data.accessible_only
        )

        if "error" in full_route_result:
            return jsonify({"error": full_route_result["error"]}), 404

        response_data = RouteResponse(**full_route_result)

        return jsonify(response_data.dict()), 200

    except Exception as e:
        return jsonify({"error": f"Route calculation failed: {e}"}), 500


@navigation_router.route('/search', methods=['GET'])
def search_locations():
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({"error": "Query parameter 'q' is required."}), 400

        # MOCK search results
        mock_results = [
            {"type": "Room", "name": f"{query} - Classroom", "location_id": 214},
            {"type": "Building", "name": "Discovery Park", "location_id": 100}
        ]
        return jsonify(mock_results), 200

    except Exception as e:
        return jsonify({"error": f"Search failed: {e}"}), 500
