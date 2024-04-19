from flask import Flask
from cryptography.fernet import Fernet
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from core.common.variables import (
    DB_NAME,
    DB_USER,
    DB_PWD,
    DB_HOST,
    DB_PORT,
    SQL_ACLCHEMY_KEY
)


# fernet key for encrypting and decrypting data
# fernet = Fernet(os.getenv("FERNET_KEY"))

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = SQL_ACLCHEMY_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    db.init_app(app)

    from core.views import home
    from core.apis import bills,dailyReport,rangeReport,pendingBills

    app.register_blueprint(home.home)
    app.register_blueprint(bills.bills)
    app.register_blueprint(dailyReport.dailyReport)
    app.register_blueprint(rangeReport.rangeReport)
    app.register_blueprint(pendingBills.pendingBills)
    
    return app
