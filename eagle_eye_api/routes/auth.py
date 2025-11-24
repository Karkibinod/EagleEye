# eagle_eye_api/routes/auth.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..services import auth_service
from ..db.session import get_db
from .schemas import UserCreate, UserLogin, Token
import json
from functools import wraps

auth_router = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


def get_db_session():
    return next(get_db())


@auth_router.route('/register', methods=['POST'])
def register_user():
    try:
        user_data = UserCreate(**request.json)
        db: Session = get_db_session()
        new_user = auth_service.create_new_user(db, user_data)

        return jsonify({
            "message": "User registered successfully.",
            "user_id": new_user.user_id,
            "role": new_user.role.value
        }), 201

    except Exception as e:
        return jsonify({"error": f"Registration failed: {e}"}), 400


@auth_router.route('/login', methods=['POST'])
def login_user():
    try:
        login_data = UserLogin(**request.json)
        db: Session = get_db_session()
        user = auth_service.authenticate_user(
            db, login_data.email, login_data.password)

        if not user:
            return jsonify({"error": "Invalid email or password."}), 401

        access_token = auth_service.create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.role.value}
        )

        return jsonify(Token(access_token=access_token, token_type="bearer").dict()), 200

    except Exception as e:
        return jsonify({"error": f"Login processing failed: {e}"}), 500
