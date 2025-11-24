# eagle_eye_api/routes/schemas.py
from typing import Optional
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

# --- User/Auth Schemas ---


class UserRoleSchema(str, Enum):
    student = "Student"
    faculty = "Faculty"
    staff = "Staff"
    visitor = "Visitor"
    admin = "Admin"


class UserCreate(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    role: UserRoleSchema = UserRoleSchema.visitor


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

# --- Navigation Schemas ---


class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_location_id: int
    accessible_only: bool = False


class NavigationStep(BaseModel):
    step: str
    floor: Optional[str] = None


class RouteResponse(BaseModel):
    outdoor_segment: dict
    indoor_segment: list[NavigationStep]
    accessible_mode: bool

# --- Event Schemas ---


class EventCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    location_id: int


class EventResponse(BaseModel):
    event_id: str
    title: str
    start_time: datetime
    end_time: datetime
    location_id: int
    organizer_id: Optional[int] = None

    class Config:
        orm_mode = True

# --- Emergency Schemas ---


class SafetyShareRequest(BaseModel):
    route_id: int
    contact_info: str


class SafetyShareResponse(BaseModel):
    share_token: str
    is_active: bool


class AlertBroadcastRequest(BaseModel):
    alert_type: str
    location_id: Optional[int] = None
    safe_zone_name: Optional[str] = None
