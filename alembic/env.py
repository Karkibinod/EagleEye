# alembic/env.py (Changes only, look for the 'config' and 'target_metadata' sections)

# Add these imports at the top (Critical for finding your modules)
from eagle_eye_api.models import user, location, route, event, emergency, building
from eagle_eye_api.db.session import Base, engine
from eagle_eye_api.config.settings import SQLALCHEMY_DATABASE_URL
import os
import sys
from os.path import abspath, dirname
# Point sys.path to your project root so Alembic can find the eagle_eye_api package
sys.path.insert(0, abspath(dirname(dirname(__file__))))

# --- Import all your models here so Alembic detects them ---

# ... (rest of the file) ...

# Replace target_metadata = None with the SQLAlchemy Base object
target_metadata = Base.metadata


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Use the SQLAlchemy URL from your settings (loaded via .env)
    connectable = engine

    # ... (rest of the run_migrations_online function) ...
