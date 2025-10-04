from functools import wraps
from flask import request, jsonify
import jwt
from models.admin import Admin
import os

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            auth_header = request.headers.get('Authorization')
            if auth_header:
                parts = auth_header.split()
                if len(parts) == 2 and parts[0] == 'Bearer':
                    token = parts[1]

            if not token:
                return jsonify({"msg": "Token is missing"}), 401

            try:
                secret = os.environ.get("SECRET_KEY")
                data = jwt.decode(token, secret, algorithms=["HS256"])
                user_id = int(data['sub'])
                current_user = Admin.query.get(user_id)
                if not current_user:
                    return jsonify({"msg": "User not found"}), 401

                allowed_roles = role if isinstance(role, list) else [role] if role else None
                if allowed_roles and current_user.role.lower() not in [r.lower() for r in allowed_roles]:
                    return jsonify({"msg": "Access forbidden: insufficient role"}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({"msg": "Token expired"}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({"msg": f"Invalid token: {str(e)}"}), 401

            return f(current_user, *args, **kwargs)
        return decorated
    return decorator
