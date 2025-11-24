# eagle_eye_api/services/routing_service.py
from googlemaps import Client as GoogleMapsClient
from sqlalchemy.orm import Session
from ..models.location import Location
from ..config.settings import GOOGLE_MAPS_API_KEY
from typing import Optional

# Initialize the Google Maps Client
gmaps = GoogleMapsClient(key=GOOGLE_MAPS_API_KEY)


def get_outdoor_route(start_coords: tuple, end_address: str) -> dict:
    """Calculates the route from GPS to the destination building address."""
    try:
        origin = f"{start_coords[0]},{start_coords[1]}"
        directions_result = gmaps.directions(
            origin=origin,
            destination=end_address,
            mode="walking",
        )
        if directions_result:
            return directions_result[0]
        else:
            return {"error": "Outdoor path not found."}

    except Exception as e:
        return {"error": f"Failed to get outdoor route: {e}"}


def get_indoor_campus_route(db: Session, start_location_id: int, end_location_id: int, accessible_only: bool = False) -> list:
    """Calculates the detailed route within the campus/building using the internal graph."""
    start_loc = db.query(Location).filter(
        Location.id == start_location_id).first()
    end_loc = db.query(Location).filter(Location.id == end_location_id).first()

    if not start_loc or not end_loc:
        return {"error": "Start or end location not found in campus database."}

    # CORE ROUTING LOGIC: Placeholder for Dijkstra/A* algorithm implementation
    mock_path = [
        {"step": "Enter the Engineering Building through the main entrance.", "floor": "1"},
        {"step": "Take the elevator to floor 2.", "floor": "2"},
        {"step": "Destination is Room 204 on your right.", "floor": "2"}
    ]

    return mock_path


def calculate_full_route(db: Session, start_coords: tuple, end_location_id: int, accessible_only: bool) -> dict:
    """Combines outdoor and indoor navigation segments."""
    final_destination = db.query(Location).filter(
        Location.id == end_location_id).first()

    if not final_destination:
        return {"error": "Final destination not found."}

    outdoor_address = final_destination.building_name + ", UNT Denton, TX"
    outdoor_result = get_outdoor_route(start_coords, outdoor_address)

    if "error" in outdoor_result:
        return outdoor_result

    # Placeholder for the building entrance ID
    building_entrance_id = 99
    indoor_result = get_indoor_campus_route(
        db, building_entrance_id, end_location_id, accessible_only)

    full_route = {
        "outdoor_segment": outdoor_result,
        "indoor_segment": indoor_result,
        "accessible_mode": accessible_only
    }
    return full_route
