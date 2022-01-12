from flask import (
    Blueprint, flash, render_template, request
)
from flask_login import current_user
from flask_mail import Message, Attachment

import datetime
import re

from webapp.utilities.variables import MAIL_REGEX, mail
from webapp.utilities import UserPerms
from webapp.db.shipment_queries import get_shipments_of_user, edit_shipment
from webapp.db.user_queries import create_account, delete_user, get_all_users
from webapp.utilities.decorators import perms_required
from webapp.utilities.utilities import verify_form, qr_loader

bp = Blueprint('admin', __name__)


@bp.route('/panel', methods=('GET', 'POST'))
@perms_required('auth.login', to_check=UserPerms.ADMIN)
def panel():
    shipment_user = request.args.get('mail')
    data_shipment = {'mail': shipment_user, 'list': get_shipments_of_user(shipment_user)}

    if request.method == "POST":
        if (request_type := request.form).get('register-user') is not None:
            user_mail = request_type.get('mail')
            password = request_type.get('password')
            perms = getattr(UserPerms, request_type.get('perms'), None)

            print(user_mail, password, perms)

            if (
                (8 <= len(password) < 20)
                and re.search(MAIL_REGEX, user_mail) is not None
                and verify_form(user_mail, password)
                and create_account(user_mail, password, perms)
            ):
                flash(f"{user_mail} è stato creato.")
            else:
                flash("Qualcosa è andato storto.")

        elif request_type.get('deleteUser') is not None:
            user_mail = request_type.get('button')
            user_type = request_type.get('valueUser')
            delete_user('trucker', user_mail) if int(user_type) != 1 else delete_user('admin', user_mail)

        elif request_type.get('editShipment') is not None:
            shipment_id = int(request_type.get('button').split()[0])
            shipment_mail = request_type.get('button').split()[1]
            shipment_plate = request_type.get('button').split()[2]
            shipment_status = int(request_type.get('shipmentStatus'))
            edit_shipment(shipment_id, shipment_status)

            if shipment_status == 0:
                msg = Message(
                    'La tua richiesta di tracking è stata accettata! Nel caso questa fosse la prima spedizione con '
                    'questo camion, appiccica il QRCode in modo che sia possibile scannerizzarlo',
                    attachments=[
                        Attachment(
                            "image.png",
                            "image/png",
                            qr_loader(f'{shipment_plate}'),
                            'inline',
                            headers=[('Content-ID', "image")]
                        )
                    ],
                    recipients=[shipment_mail]
                )
                mail.send(msg)

    return render_template(
        'users/panel.html',
        title="Admin page",
        users=get_all_users(),
        shipments=data_shipment,
        user=current_user,
        current_date=datetime.date.today()
    )
