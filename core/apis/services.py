from flask import Blueprint, jsonify, request
from core import db

from core.models import ServiceItem


services = Blueprint('services', __name__)


@services.route('/api/new/service/number', methods=['GET'])
def get_new_service_number():
    service = ServiceItem.query.order_by(ServiceItem.id.desc()).first()
    if not service:
        return jsonify({'serviceNumber': 1})
    
    return jsonify({'serviceNumber': service.id + 1})


@services.route('/api/add/service', methods=['POST'])
def add_service():
    data = request.get_json()
    service = ServiceItem(**data)
    db.session.add(service)
    db.session.commit()
    return jsonify({'message': 'Service added successfully'})
