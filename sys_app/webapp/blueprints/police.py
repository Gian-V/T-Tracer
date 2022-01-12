from flask import (
    Blueprint, render_template, abort
)
from jinja2 import Template

import folium
import re
import datetime

from webapp.utilities import UserPerms
from webapp.utilities.decorators import police_required, perms_required
from webapp.db.shipment_queries import get_shipments_by_plate, get_gps_log_by_id
from webapp.utilities.utilities import generate_geo_list
from webapp.utilities.variables import PLATE_REGEX

bp = Blueprint('police', __name__)


@bp.route('/path-home')
@perms_required('auth.login', to_check=UserPerms.POLICE)
def path_home():
    return """
    <script>
        let node = document.createElement("title");
        let textnode = document.createTextNode("Path Home");
        node.appendChild(textnode);
        document.querySelector("head").appendChild(node);
        let node2 = document.createElement("link");
        node2.setAttribute("rel", "icon");
        node2.setAttribute("type", "image/x-icon");
        node2.setAttribute("href", "static/img/favicon.png");
        document.querySelector("head").appendChild(node2);
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
    """


@bp.route('/path-<look_id>', methods=('GET', 'POST'))
@police_required
def path(look_id: str):
    if re.search(PLATE_REGEX, look_id.upper()) is None:
        abort(404)

    return render_template(
        'users/path.html',
        title="Path",
        shipments_list=get_shipments_by_plate(look_id.upper()),
        current_date=datetime.date.today()
    )


@bp.route('/gps_log/<int:_id>')
@perms_required('auth.login', to_check=UserPerms.POLICE)
def gps_getter(_id: int):

    if (gps_log := get_gps_log_by_id(_id)) is None or not gps_log:
        abort(404)

    marks_list = generate_geo_list(gps_log)

    geo_map = folium.Map(location=[*marks_list[0].location], zoom_start=15)

    for i in marks_list:
        folium.Marker(*[i.location], popup=f'Ore {i.date}').add_to(geo_map)

    folium.PolyLine(locations=[i.location for i in marks_list], line_opacity=0.5).add_to(geo_map)

    template = Template(f"""
    <script>
        let node = document.createElement("title");
        let textnode = document.createTextNode("GPS");
        node.appendChild(textnode);
        document.querySelector("head").appendChild(node);
    </script>
    {geo_map._repr_html_()}
    """)

    return template.render()
