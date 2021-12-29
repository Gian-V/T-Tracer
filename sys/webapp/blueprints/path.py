from flask import (
    Blueprint
)

from webapp.utilities.decorators import police_required

bp = Blueprint('path', __name__)


@bp.route('/path-home')
def path_home():
    return "You are logged as Police"


@bp.route('/path-<look_id>', methods=('GET', 'POST'))
# @police_required
def path(look_id):
    return look_id
