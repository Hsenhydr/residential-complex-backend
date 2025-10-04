from flask import Blueprint, request, jsonify
from models.admin import Admin
import jwt
import os
from datetime import datetime, timedelta
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/login')

@auth_bp.route('', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    user = Admin.query.filter_by(email=email, password=password).first()
    
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    payload = {
        "fresh": False,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "type": "access",
        "sub": str(user.id),
        "role": user.role,   
        "nbf": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    token = jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")

    return jsonify({"access_token": token})
