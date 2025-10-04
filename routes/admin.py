from flask import Blueprint, request, jsonify
from models.admin import Admin
from extensions import db
from utils import token_required 

admins_bp = Blueprint('admins', __name__, url_prefix='/admins')

@admins_bp.route('', methods=['GET'])
@token_required(role=['Admin','SuperAdmin'])
def get_admins(current_user):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')

    query = Admin.query
    if search:
        query = query.filter(
            (Admin.first_name.like(f'%{search}%')) | 
            (Admin.last_name.like(f'%{search}%')) | 
            (Admin.email.like(f'%{search}%'))
        )

    pagination = query.paginate(page=page, per_page=per_page)
    admins = [{
        "id": a.id,
        "civility": a.civility,
        "first_name": a.first_name,
        "last_name": a.last_name,
        "email": a.email,
        "phone": a.phone,
        "role": a.role,
        "status": a.status,
        "password": a.password
    } for a in pagination.items]

    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "admins": admins
    })


@admins_bp.route('', methods=['POST'])
@token_required(role='SuperAdmin')
def add_admin(current_user):
    data = request.json
    admin = Admin(
        civility=data['civility'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        role=data['role'],
        status=data['status'],
        password=data['password']
    )
    db.session.add(admin)
    db.session.commit()
    return jsonify({"msg": "Admin added", "id": admin.id}), 201
