from core import db

class Customer(db.Model):
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    mobile_number = db.Column(db.String(15))

class VehicleHistory(db.Model):
    __tablename__ = 'vehicle_history'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle_km = db.Column(db.Integer)
    next_km = db.Column(db.Integer)
    
    vehicle = db.relationship('Vehicle', backref=db.backref('history', lazy=True))


# Define the Vehicle model
class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20))

# Define the ServiceItem model
class ServiceItem(db.Model):
    __tablename__ = 'service_item'
    
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(255))
    item_unit = db.Column(db.String(50))
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}    

# Define the Bill model
class Bill(db.Model):
    __tablename__ = 'bill'
    
    id = db.Column(db.String, primary_key=True)
    bill_date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle_history_id = db.Column(db.Integer, db.ForeignKey('vehicle_history.id'))
    discount_amount = db.Column(db.Float)
    is_paid = db.Column(db.Boolean)
    total_amount = db.Column(db.Float)
    customer = db.relationship('Customer', backref=db.backref('bills', lazy=True))
    vehicle = db.relationship('Vehicle', backref=db.backref('bills', lazy=True))
    vehicle_history = db.relationship('VehicleHistory', backref=db.backref('bills', lazy=True))
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}    


# Define the BillServiceItemMapping model
class BillServiceItemMapping(db.Model):
    __tablename__ = 'bill_service_item_mapping'
    bill_id = db.Column(db.String, db.ForeignKey('bill.id'), primary_key=True)
    service_item_id = db.Column(db.Integer, db.ForeignKey('service_item.id'), primary_key=True)
    item_rate = db.Column(db.Float)
    item_quantity = db.Column(db.Integer)
    bill = db.relationship('Bill', backref=db.backref('service_items', lazy=True))
    service_item = db.relationship('ServiceItem', backref=db.backref('bills', lazy=True))

