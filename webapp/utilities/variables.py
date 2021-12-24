from flask_mail import Mail
from flask_login import LoginManager
from webapp.db.db_class import SQLOperation


mail = Mail()
sqldb = SQLOperation()
