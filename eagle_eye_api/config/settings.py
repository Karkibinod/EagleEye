# eagle_eye_api/config/settings.py (FIXED)
import os
from dotenv import load_dotenv

# Load environment variables from the project root's .env file
load_dotenv()

# --- Database & API Credentials ---
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# --- Security Configuration ---
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# REMOVED: from ..models.location import Location
# This import caused the circular dependency loop.
