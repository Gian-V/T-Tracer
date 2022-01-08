from flask import (
    Blueprint, render_template, request, flash
)
from flask_mail import Message
from flask_login import current_user

import re
import datetime

from webapp.utilities.decorators import perms_required
from webapp.db.user_queries import get_request_count
from webapp.db.shipment_queries import create_shipment
from webapp.utilities.utilities import verify_form
from webapp.utilities.variables import PLATE_REGEX, mail

bp = Blueprint('main', __name__)


@bp.route('/', methods=('GET', 'POST'))
@perms_required('auth.login', to_check=None)
def index():
    if request.method == "POST":
        plate = request.form.get('plate').upper()
        start_where = request.form.get('form_start')
        end_where = request.form.get('form_end')
        try:
            goods_weight = round(float(request.form.get('goods_weight')))
            start_date = datetime.datetime.strptime(request.form.get('date_start'), "%d/%m/%Y").date()
            end_date = datetime.datetime.strptime(request.form.get('date_end'), "%d/%m/%Y").date()
        except ValueError:
            goods_weight = 0
            start_date = ""
            end_date = ""
        goods_type = request.form.get('textarea')

        if (
            start_date <= end_date and goods_weight > 0 and re.search(PLATE_REGEX, plate) is not None
            and verify_form(plate, start_where, end_where, start_date, end_date, end_date, goods_type)
            and get_request_count(current_user.mail)
        ):
            create_shipment(
                current_user.mail,
                plate,
                start_date,
                end_date,
                start_where,
                end_where,
                goods_type,
                goods_weight
            )
            msg = Message(
                f"{current_user.mail} has just sent a request for our service, check it out.",
                recipients=[]
            )
            msg.add_recipient(msg.sender)
            mail.send(msg)
            flash("Request sent correctly")
        else:
            flash("Some fields are missing or you reached the max request per month")

    return render_template('index.html', title="Index")
