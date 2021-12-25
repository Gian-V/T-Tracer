from flask import (
    Blueprint, render_template, request, flash
)
from flask_mail import Message
from webapp.utilities.utilities import send_document
from webapp.utilities.decorators import join_required
from webapp.utilities.variables import mail

bp = Blueprint('main', __name__)


@bp.route('/', methods=('GET', 'POST'))
@join_required('auth.login', to_check=None)
def index():
    if request.method == "POST":
        car_id = request.form.get('id')
        to_start = request.form.get('start')
        to_arrive = request.form.get('arrive')
        email = request.form.get('mail')

        if (sent_request := send_document(car_id, to_start, to_arrive, email))[0]:
            msg = Message(
                "Ciao",
                recipients=["ferrari.lorenzo04@gmail.com"]
            )
            mail.send(msg)

        flash(sent_request[1])

    return render_template('index.html', title="Index")
