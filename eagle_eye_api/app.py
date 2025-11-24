# eagle_eye_api/app.py
from flask import Flask, jsonify
from .routes.auth import auth_router
from .routes.navigation import navigation_router
from .routes.event import event_router
from .routes.emergency import emergency_router
from .db.session import engine, Base
from .config.settings import SECRET_KEY


def create_app():
    """Factory function to create and configure the Flask application instance."""
    app = Flask(__name__)

    # --- 1. Configuration ---
    app.config['SECRET_KEY'] = SECRET_KEY

    # --- 2. Database Initialization ---
    # NOTE: In production, Alembic manages migrations. This is removed for migration control.

    app.logger.info(
        "Database engine initialized. Run 'alembic upgrade head' to apply migrations.")

    # --- 3. Register Blueprints (Routes) ---
    app.register_blueprint(auth_router)
    app.register_blueprint(navigation_router)
    app.register_blueprint(event_router)
    app.register_blueprint(emergency_router)

    # --- 4. Error Handling ---
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found", "message": "The requested URL was not found on the server."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
