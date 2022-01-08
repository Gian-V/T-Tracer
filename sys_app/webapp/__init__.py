from flask import Flask
from flask_login import LoginManager

import json

from webapp.blueprints.auth import User
from webapp.utilities.variables import mail, sqldb
from webapp.blueprints import index, auth, path
from webapp.blueprints.errors import error_404
from webapp.db.user_queries import get_user_by_mail

blueprints = [index.bp, auth.bp, path.bp]
error_handler = [(404, error_404)]


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)

    mail.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_mail: str):
        obj = get_user_by_mail(user_mail)
        if obj is None:
            return None
        return User(obj.id, obj.mail, obj.password, getattr(obj, 'perms', None))

    sqldb.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)

    for e in error_handler:
        app.register_error_handler(*e)

    app.add_url_rule('/', endpoint='index')

    app.config.from_pyfile('config.py', silent=True) if test_config is None else app.config.from_mapping(test_config)

    return app
