from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user

import datetime


from webapp.utilities import UserPerms
from webapp.utilities import User
from webapp.utilities.decorators import perms_required, route_redirect
from webapp.utilities.utilities import verify_form
from webapp.db.user_queries import check_user_login

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
@route_redirect
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
                return redirect(url_for('user.user_request'))

            elif account[1].perms == UserPerms.POLICE:
                if path_id is not None:
                    return redirect(url_for('police.path', look_id=path_id))
                return redirect(url_for('police.path_home'))

            elif account[1].perms == UserPerms.ADMIN:
                return redirect(url_for('admin.panel'))

        flash("Credenziali non valide")

    return render_template('auth/login.html', title="Login page")


@bp.route('/logout', methods=('GET', 'POST'))
@perms_required('auth.login', to_check=[None, UserPerms.ADMIN, UserPerms.POLICE])
def logout():
    logout_user()
    return """
    <script>
        let node = document.createElement("title");
        let textnode = document.createTextNode("Logout");
        node.appendChild(textnode);
        document.querySelector("head").appendChild(node);
    </script>
    Logging out...
    """, {"Refresh": "3; url=login"}
