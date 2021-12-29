from flask import (
    Blueprint, render_template, request, flash
)
from flask_mail import Message, Attachment

import datetime

from webapp.utilities.decorators import perms_required
from webapp.utilities.utilities import verify_form, qr_loader
from webapp.utilities.variables import mail

bp = Blueprint('main', __name__)


@bp.route('/', methods=('GET', 'POST'))
@perms_required('auth.login', to_check=None)
def index():
    if request.method == "POST":
        plate = request.form.get('id')
        start_where = request.form.get('where_start')
        end_where = request.form.get('where_end')
        try:
            start_date = datetime.datetime.strptime(request.form.get('date_start'), "%d/%m/%Y").date()
            end_date = datetime.datetime.strptime(request.form.get('date_end'), "%d/%m/%Y").date()
        except ValueError as e:
            start_date = ""
            end_date = ""
        goods_type = request.form.get('goods')
        goods_weight = request.form.get('goods_weight')

        if verify_form(plate, start_where, end_where, start_date, goods_type, end_date):
            msg = Message(
                'ciao',
                attachments=[Attachment("image.png", "image/png", qr_loader('https://www.google.com'), 'inline', headers=[('Content-ID', 'image')])],
                recipients=["ferrari.lorenzo04@gmail.com"]
            )
            mail.send(msg)
        else:
            flash("Some fields are missing or you reached the max request per month")

    return render_template('index.html', title="Index")
