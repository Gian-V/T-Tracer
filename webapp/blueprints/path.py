from flask import (
    Blueprint
)
from flask_login import login_required

bp = Blueprint('path', __name__)


@bp.route('/path-<int:look_id>', methods=('GET', 'POST'))
@login_required
def path(look_id: int):
    return str(look_id)
