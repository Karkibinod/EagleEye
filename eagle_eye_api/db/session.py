# eagle_eye_api/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..config.settings import SQLALCHEMY_DATABASE_URL

# The engine manages the core connectivity to the DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

# The session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """Dependency function to get and close a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
