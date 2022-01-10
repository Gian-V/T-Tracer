from flask import (
    Blueprint, render_template, abort
)
from jinja2 import Template

import re
import datetime

from webapp.utilities import UserPerms
from webapp.utilities.decorators import police_required, perms_required
from webapp.db.shipment_queries import get_shipments_by_plate, get_gps_log_by_id
from webapp.utilities.variables import PLATE_REGEX

bp = Blueprint('path', __name__)


@bp.route('/path-home')
@perms_required('auth.login', to_check=UserPerms.POLICE)
def path_home():
    template = Template("""
    <script>
        var node = document.createElement("title");
        var textnode = document.createTextNode("Path Home");
        node.appendChild(textnode);
        document.querySelector("head").appendChild(node);
    </script>
    <style>
        .container {
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            position: fixed;
        }
    </style>
    <div class="container">
        <h1>Hai fatto l'accesso come poliziotto</h1>
    </div>
    """)

    return template.render(title="Path Home")


@bp.route('/path-<look_id>', methods=('GET', 'POST'))
@police_required
def path(look_id: str):
    if re.search(PLATE_REGEX, look_id.upper()) is None:
        abort(404)

    return render_template(
        'path.html',
        title="Path",
        shipments_list=get_shipments_by_plate(look_id.upper()),
        current_date=datetime.date.today()
    )


@bp.route('/gps_log/<int:_id>')
@perms_required('auth.login', to_check=UserPerms.POLICE)
def gps_getter(_id: int):

    gps_log = get_gps_log_by_id(_id)
    if gps_log is None:
        abort(404)

    template = Template("""
    <script>
        var node = document.createElement("title");
        var textnode = document.createTextNode("GPS");
        node.appendChild(textnode);
        document.querySelector("head").appendChild(node);
    </script>
    {% for i in gps_log.split("-")[:-1] %}
        <p>{{ i }}</p>
    {% endfor %}
    """)

    return template.render(title="GPS", gps_log=gps_log)
