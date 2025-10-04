from flask import Blueprint, request, jsonify
from models.building import Building
from models.residential_complex import ResidentialComplex
from models.admin import Admin
from extensions import db
from utils import token_required

buildings_bp = Blueprint('buildings', __name__, url_prefix='/buildings')

@buildings_bp.route('', methods=['GET'])
@token_required(role=['Admin', 'SuperAdmin'])
def get_buildings(current_user):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')

    query = Building.query.join(ResidentialComplex)
    if search:
        query = query.filter(
            Building.name.like(f"%{search}%") |
            ResidentialComplex.identity.like(f"%{search}%")
        )

    pagination = query.paginate(page=page, per_page=per_page)
    buildings = [{
        "id": b.id,
        "name": b.name,
        "complex_id": b.complex_id,
        "admin_id": b.admin_id
    } for b in pagination.items]

    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "buildings": buildings
    })

@buildings_bp.route('', methods=['POST'])
@token_required(role='SuperAdmin')
def add_building(current_user):
    data = request.json
    building = Building(
        name=data['name'],
        complex_id=data['complex_id']
    )
    db.session.add(building)
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

        building.admin_id = admin.id
        db.session.commit()

    return jsonify({"msg": "Building added", "id": building.id}), 201

@buildings_bp.route('/<int:id>', methods=['DELETE'])
@token_required(role='SuperAdmin')
def delete_building(current_user, id):
    building = Building.query.get_or_404(id)
    db.session.delete(building)
    db.session.commit()
    return jsonify({"msg": "Building deleted"}), 200
