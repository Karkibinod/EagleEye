from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, String, Enum as SqlAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from ..db.session import Base

# Define an Enum for user roles (SRS: Students, Faculty, Staff, Visitor)


class UserRole(enum.Enum):
    STUDENT = "Student"
    FACULTY = "Faculty"
    STAFF = "Staff"
    VISITOR = "Visitor"
    ADMIN = "Admin"


class User(Base):
    """
    Database Model for User Authentication and Profile Information.
    Implements role-based access control and stores hashed credentials.
    """
    __tablename__ = "users"

    # Core Identifiers and Attributes (SRS: userID, name, role)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    # Used for login/visitor identity
    email = Column(String, unique=True, index=True, nullable=False)

    # Authentication Data (SRS: password: Stnring, encrypted)
    hashed_password = Column(String, nullable=False)

    # Role-Based Access Control (SRS: role: Enum)
    role = Column(SqlAlchemyEnum(UserRole),
                  default=UserRole.VISITOR, nullable=False)

    # Relationship to Preferences (defined below)
    preferences_id = Column(Integer, ForeignKey(
        "preferences.id"), nullable=True)
    preferences = relationship(
        "Preferences", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', role='{self.role.value}')>"


class Preferences(Base):
    """
    Database Model for storing user settings and preferences.
    Manages accessibility needs and notification settings.
    """
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)

    # Accessibility Features (SRS: accessibilityMode)
    accessibility_mode_enabled = Column(Boolean, default=False, nullable=False)

    # Notifications (SRS: notification settings)
    notifications_enabled = Column(Boolean, default=True, nullable=False)

    # Relationship back to the User
    user_id = Column(Integer, ForeignKey("users.id"),
                     unique=True, nullable=False)
    user = relationship("User", back_populates="preferences")
