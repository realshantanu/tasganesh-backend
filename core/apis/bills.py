from flask import Blueprint, jsonify, request
from sqlalchemy import String, cast, desc
from core import db
from core.decorators import serialize_data
from datetime import datetime
from core.models import (
    Bill,
    BillServiceItemMapping,
    Customer,
    ServiceItem,
    Vehicle,
    VehicleHistory
)

bills = Blueprint('bills', __name__)

@serialize_data
@bills.route('/api/service/names', methods=['GET'])
def get_service_names():
    items = ServiceItem.query.all()
    return jsonify([item.to_dict() for item in items])



@serialize_data
@bills.route('/api/new/bill/number',methods=['GET'])
def get_new_bill_number():
    all_bills = Bill.query.all()
    last_bill = sorted(all_bills, key=lambda bill: int(bill.id.split('/')[0]), reverse=True)[0]
    current_year = datetime.now().year
    next_year = current_year + 1 if datetime.now().month > 3 else current_year
    financial_year = f"{str(current_year)[-2:]}-{str(next_year)[-2:]}"
    
    if last_bill:
        last_bill_number = last_bill.id
        last_bill_number_parts = last_bill_number.split('/')
        if last_bill_number_parts[1] != financial_year:
            new_bill_number = f"1/{financial_year}"
        else:
            new_bill_number = f"{int(last_bill_number_parts[0]) + 1}/{financial_year}"
    else:
        new_bill_number = f"1/{financial_year}"  # Default bill number if no bills exist yet
    return jsonify(new_bill_number=new_bill_number)

@serialize_data
@bills.route('/api/vehicles/<string:vehicle_number>/bills', methods=['GET'])
def get_vehicle_bills(vehicle_number):
    vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404

    bills = Bill.query.filter_by(vehicle_id=vehicle.id, is_paid=False).all()
    result = []
    for bill in bills:
        result.append({
            'billno': bill.id,
            'name': bill.customer.name,
            'amount': bill.total_amount,
            'dueDate': bill.bill_date.strftime('%Y-%m-%d'),
            'status': 'Paid' if bill.is_paid else 'Unpaid'
        })
    return jsonify(result)


@serialize_data
@bills.route('/api/vehicles/<string:vehicle_number>/history', methods=['GET'])
def get_vehicle_history(vehicle_number):
    vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    
    data = db.session.query(
        Bill.id.label('billId'),
        cast(Bill.bill_date, String).label('billDate'),
        VehicleHistory.vehicle_km.label('vehicleKm')
    ).join(
        VehicleHistory, 
        Bill.vehicle_history_id == VehicleHistory.id
    ).filter(
        Bill.vehicle_id == vehicle.id
    ).all()

    result = [row._asdict() for row in data]

    return jsonify(result)
    

@serialize_data
@bills.route('/api/bill/create', methods=['POST'])
def create_bill():
    data = request.get_json()
    
    customer = Customer.query.filter_by(mobile_number=data['mobileNumber']).first()
    if not customer:
        customer = Customer(name=data['customer'], address=data['address'], mobile_number=data['mobileNumber'])
        db.session.add(customer)
    
    vehicle = Vehicle.query.filter_by(vehicle_number=data['vehicleNumber']).first()
    if not vehicle:
        vehicle = Vehicle(vehicle_number=data['vehicleNumber'])
        db.session.add(vehicle)
    
    db.session.flush()
    

    # Create a vehicle history entry
    vehicle_history = VehicleHistory(vehicle_id=vehicle.id, vehicle_km=data['vehicleKm'], next_km=data['nextKm'])
    db.session.add(vehicle_history)
    
    db.session.flush()

    
    bill = Bill(
        id=data['billNumber'],
        bill_date=datetime.strptime(data['currentDate'], '%Y-%m-%d'),
        customer_id=customer.id,
        vehicle_id=vehicle.id,
        discount_amount=data['selectDiscountAmount'],
        is_paid=data['selectPaidBool'],
        total_amount=data['totalAmount'],
        vehicle_history_id=vehicle_history.id
    )
    db.session.add(bill)
    
    for service in data['services']:
        service_item = ServiceItem.query.filter_by(service_name=service['serviceName']).first()
        if service_item:
            bill_service_item_mapping = BillServiceItemMapping(bill_id=bill.id, 
                                                               service_item_id=service_item.id, 
                                                               item_rate = service['itemRate'],
                                                               item_quantity=service['itemQuantity'])
            db.session.add(bill_service_item_mapping)

    db.session.commit()
    db.session.commit()
    return jsonify('Bill generated!')

