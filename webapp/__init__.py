from flask import Flask
from flask_login import LoginManager
from flask_qrcode import QRcode

from webapp.blueprints.auth import User
from webapp.db.user_queries import get_user_by_username
from webapp.utilities.variables import mail, sqldb
import json
from webapp.blueprints import index, auth, path
# from webapp.errors.errors import error_404

blueprints = [index.bp, auth.bp, path.bp]
# error_handler = [(404, error_404)]

with open("webapp/token.json", "r") as f:
    data = json.load(f)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = data["secret_key"]
    app.config['SESSION_TYPE'] = data["session_type"]
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE='webapp/databswqsase.db'
    # )

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'pydb.testing@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Qazwsx12@'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    QRcode(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(username: str):
        obj = get_user_by_username(username)
        if obj is None:
            return None
        return User(obj.id, obj.username, obj.password, getattr(obj, 'perms', None))

    sqldb.init_app('TTRW', 'jArkqhHW2cJNSLD8', '64.225.96.112', 3306, 'T_Tracer')

    for bp in blueprints:
        app.register_blueprint(bp)

    # for e in error_handler:
    #     app.register_error_handler(*e)

    app.add_url_rule('/', endpoint='index')

    app.config.from_pyfile('config.py', silent=True) if test_config is None else app.config.from_mapping(test_config)

    return app
