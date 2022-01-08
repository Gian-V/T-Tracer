from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from flask_mail import Message, Attachment
from flask_login import login_user, logout_user, current_user

import re
import datetime


from webapp.utilities import UserPerms
from webapp.utilities import User
from webapp.utilities.decorators import perms_required
from webapp.utilities.utilities import verify_form, qr_loader
from webapp.utilities.variables import MAIL_REGEX, mail
from webapp.db.user_queries import check_user_login, create_account, delete_user, get_all_users
from webapp.db.shipment_queries import edit_shipment, get_shipments_of_user

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        user_mail = request.form.get('mail')
        password = request.form.get('password')

        if verify_form(user_mail, password) and (account := check_user_login(user_mail, password))[0]:
            path_id = session.get('path', None)
            session.clear()

            login_user(User(
                account[1].id,
                account[1].mail,
                account[1].password,
                getattr(account[1], 'perms', None)
            ), duration=datetime.timedelta(days=1))

            if getattr(account[1], 'perms', None) is None:
                return redirect(url_for('index'))

            elif account[1].perms == UserPerms.POLICE:
                if path_id is not None:
                    return redirect(url_for('path.path', look_id=path_id))
                return redirect(url_for('path.path_home'))

            elif account[1].perms == UserPerms.ADMIN:
                return redirect(url_for('auth.panel'))

        flash("Invalid credentials")

    return render_template('auth/login.html', title="Login page")


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
                flash(f"{user_mail} has been created")
            else:
                flash("Something went wrong")

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
                    'Your shipment has been accepted! In case this is the first shipment with'
                    'this truck Here it is your qrcode',
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
        'auth/panel.html',
        title="Admin page",
        users=get_all_users(),
        shipments=data_shipment,
        user=current_user,
        current_date=datetime.date.today()
    )


@bp.route('/logout', methods=('GET', 'POST'))
@perms_required('auth.login', to_check=[None, UserPerms.ADMIN, UserPerms.POLICE])
def logout():
    logout_user()
    return "Logging out...", {"Refresh": "3; url=login"}
