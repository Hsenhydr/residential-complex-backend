from flask import Blueprint, request, jsonify
from models.residential_complex import ResidentialComplex
from models.admin import Admin
from extensions import db
from sqlalchemy import or_
from utils import token_required

complexes_bp = Blueprint('complexes', __name__, url_prefix='/complexes')

@complexes_bp.route('', methods=['GET'])
@token_required(role=['Admin', 'SuperAdmin'])
def get_complexes(current_user):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')

    query = ResidentialComplex.query
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                ResidentialComplex.identity.like(search_pattern),
                ResidentialComplex.address.like(search_pattern)
            )
        )

    pagination = query.paginate(page=page, per_page=per_page)
    complexes = [{
        "id": c.id,
        "identity": c.identity,
        "address": c.address,
        "campaign_info": c.campaign_info
    } for c in pagination.items]

    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "complexes": complexes
    })

@complexes_bp.route('', methods=['POST'])
@token_required(role='SuperAdmin')
def add_complex(current_user):
    data = request.json
    complex_ = ResidentialComplex(
        identity=data['identity'],
        address=data['address'],
        campaign_info=data.get('campaign_info')
    )
    db.session.add(complex_)
    db.session.commit()
    
    admin_data = data.get('admin')
    if admin_data:
        admin = Admin(
            civility=admin_data.get('civility', 'Mr/Ms'),
            first_name=admin_data['first_name'],
            last_name=admin_data['last_name'],
            email=admin_data['email'],
            phone=admin_data.get('phone'),
            role='Admin',
            status='active',
            password=admin_data['password']
        )
    db.session.add(admin)
    db.session.commit()

    complex_.admin_id = admin.id
    db.session.commit()

    return jsonify({"msg": "Residential Complex added", "id": complex_.id}), 201
