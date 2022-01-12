from flask import Blueprint

from webapp.utilities.decorators import route_redirect

bp = Blueprint('main', __name__)


@bp.route('/')
@route_redirect
def index():
    pass
