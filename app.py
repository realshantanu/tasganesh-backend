from waitress import serve
from core import create_app,db
from core.models import (
    Customer,
    Vehicle,
    ServiceItem,
    Bill,
    BillServiceItemMapping,
    VehicleHistory
)

mode = 'prod'

app = create_app()

with app.app_context():
    # db.reflect()
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    if (mode == 'dev'):
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app, host='0.0.0.0', port=8000, threads=4)
