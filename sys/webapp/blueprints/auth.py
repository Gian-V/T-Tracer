from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from flask_login import login_required, login_user, logout_user, current_user

from datetime import timedelta

from webapp.utilities import UserPerms
from webapp.utilities.decorators import perms_required
from webapp.utilities.login_manager import User
from webapp.utilities.utilities import verify_form
from webapp.db.user_queries import check_user_login, create_account, delete_user, get_all_users
from webapp.db.shipment_queries import get_shipment_of_user
from collections import namedtuple

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if verify_form(username, password) and (account := check_user_login(username, password))[0]:
            path_id = session.get('path', None)
            session.clear()

            login_user(User(
                account[1].id,
                account[1].username,
                account[1].password,
                getattr(account[1], 'perms', None)
            ), duration=timedelta(days=1))

            if getattr(account[1], 'perms', None) is None:
                return redirect(url_for('index'))

            elif account[1].perms == UserPerms.POLICE:
                if path_id is not None:
                    return redirect(url_for('path', look_id=path_id))
                return redirect(url_for('path'))

            elif account[1].perms == UserPerms.ADMIN:
                return redirect(url_for('auth.panel'))

        flash("Invalid credentials")

    return render_template('auth/login.html', title="Login page")


@bp.route('/panel', methods=('GET', 'POST'))
@perms_required('auth.login', to_check=UserPerms.ADMIN)
def panel():
    shipment_user = request.args.get('username')
    data_shipment = {'username': shipment_user, 'list': get_shipment_of_user(shipment_user)}

    if request.method == "POST":
        if (request_type := request.form).get('register-user') is not None:
            username = request_type.get('username')
            password = request_type.get('password')
            perms = getattr(UserPerms, request_type.get('perms'), None)

            if (6 > len(username) > 16) and (6 > len(password) > 16)\
                    and verify_form(username, password) and create_account(username, password, perms):
                flash(f"{username} has been created")
            else:
                flash("Something went wrong")

        elif request_type.get('deleteUser') is not None:
            username = request_type.get('button')
            user_type = request_type.get('valueUser')

            if int(user_type) == 1:
                delete_user('admin', username)
            else:
                delete_user('trucker', username)

    return render_template(
        'auth/panel.html',
        title="Admin page",
        users=get_all_users(),
        shipments=data_shipment,
        user=current_user
    )


@bp.route('/logout', methods=('GET', 'POST'))
@perms_required('auth.login', to_check=[None, UserPerms.ADMIN, UserPerms.POLICE])
def logout():
    logout_user()
    return "Logging out...", {"Refresh": "3; url=login"}
