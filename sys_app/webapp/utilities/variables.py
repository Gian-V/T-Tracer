from flask_mail import Mail

from webapp.db import SQLOperation


MAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
PLATE_REGEX = r'^[A-Z]{2}[0-9]{3}[A-Z]{2}$'

mail = Mail()
sqldb = SQLOperation()
