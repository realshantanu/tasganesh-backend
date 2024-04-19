from flask import Blueprint, jsonify

pendingBills = Blueprint('pendingBills', __name__)  
from core.models import Bill


@pendingBills.route('/report/pending', methods=['GET'])
def get_pending_bills():

    pending_bills = Bill.query.filter_by(is_paid=False).all()
    total_unpaid_bills = len(pending_bills)
    total_unpaid_earnings = sum(bill.total_amount for bill in pending_bills)

    pending_bills_details = [{
        'bill_no': bill.id,
        'customer': bill.customer.name,
        'amount': bill.total_amount,
        'status': 'Unpaid'
    } for bill in pending_bills]

    return jsonify({
        'total_unpaid_bills': total_unpaid_bills,
        'total_unpaid_earnings': total_unpaid_earnings,
        'pending_bills_details': pending_bills_details
    })
