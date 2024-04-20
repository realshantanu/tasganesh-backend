from flask import Blueprint, jsonify, request
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from sqlalchemy import func

from core.models import (
    Bill, ServiceItem, Vehicle, Customer, VehicleHistory, BillServiceItemMapping
    )


rangeReport = Blueprint('rangeReport', __name__)

@rangeReport.route('/report/range', methods=['GET'])
def get_range_report():
    from_date_str = request.args.get('from_date')
    to_date_str = request.args.get('to_date')

    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else datetime.today().date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if to_date_str else datetime.today().date()

    total_services = ServiceItem.query.join(BillServiceItemMapping).join(Bill).filter(Bill.bill_date.between(from_date, to_date)).count()
    total_vehicles = Vehicle.query.join(Bill).filter(Bill.bill_date.between(from_date, to_date)).count()
    total_bills = Bill.query.filter(Bill.bill_date.between(from_date, to_date)).count()
    bills_paid = Bill.query.filter_by(is_paid=True).filter(Bill.bill_date.between(from_date, to_date)).count()
    bills_unpaid = Bill.query.filter_by(is_paid=False).filter(Bill.bill_date.between(from_date, to_date)).count()
    total_earnings = Bill.query.filter(Bill.bill_date.between(from_date, to_date)).with_entities(func.sum(Bill.total_amount)).scalar()

    bills = Bill.query.filter(Bill.bill_date.between(from_date, to_date)).all()
    
    # Get the first and last day of the prior month
    first_day_prior_month = from_date.replace(day=1) - relativedelta(months=1)
    last_day_prior_month = to_date.replace(day=1) - timedelta(days=1)

    # Get the counts for the prior month
    prior_total_services = ServiceItem.query.join(BillServiceItemMapping).join(Bill).filter(Bill.bill_date.between(first_day_prior_month, last_day_prior_month)).count()
    prior_total_vehicles = Vehicle.query.join(Bill).filter(Bill.bill_date.between(first_day_prior_month, last_day_prior_month)).count()
    prior_total_bills = Bill.query.filter(Bill.bill_date.between(first_day_prior_month, last_day_prior_month)).count()
    prior_bills_paid = Bill.query.filter_by(is_paid=True).filter(Bill.bill_date.between(first_day_prior_month, last_day_prior_month)).count()
    prior_bills_unpaid = Bill.query.filter_by(is_paid=False).filter(Bill.bill_date.between(first_day_prior_month, last_day_prior_month)).count()
    prior_total_earnings = Bill.query.filter(Bill.bill_date.between(first_day_prior_month, last_day_prior_month)).with_entities(func.sum(Bill.total_amount)).scalar()
    
    # Calculate the percentage change
    services_change = ((total_services - prior_total_services) / prior_total_services) * 100 if prior_total_services else 0
    vehicles_change = ((total_vehicles - prior_total_vehicles) / prior_total_vehicles) * 100 if prior_total_vehicles else 0
    bills_change = ((total_bills - prior_total_bills) / prior_total_bills) * 100 if prior_total_bills else 0
    paid_bills_change = ((bills_paid - prior_bills_paid) / prior_bills_paid) * 100 if prior_bills_paid else 0
    unpaid_bills_change = ((bills_unpaid - prior_bills_unpaid) / prior_bills_unpaid) * 100 if prior_bills_unpaid else 0
    earnings_change = ((total_earnings - prior_total_earnings) / prior_total_earnings) * 100 if prior_total_earnings else 0
    
    bills_details = [{
        'bill_no': bill.id,
        'customer': bill.customer.name,
        'amount': bill.total_amount,
        'status': 'Paid' if bill.is_paid else 'Unpaid',
        'vehicle_number': bill.vehicle.vehicle_number
    } for bill in bills]

    return jsonify({
        'total_services': total_services,
        'total_vehicles': total_vehicles,
        'total_bills': total_bills,
        'bills_paid': bills_paid,
        'bills_unpaid': bills_unpaid,
        'total_earnings': total_earnings,
        'bills_details': bills_details,
        'services_change': services_change,
        'vehicles_change': vehicles_change,
        'bills_change': bills_change,
        'paid_bills_change': paid_bills_change,
        'unpaid_bills_change': unpaid_bills_change,
        'earnings_change': earnings_change
    })