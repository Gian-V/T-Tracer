from flask import (
    redirect, url_for, session
)
from flask_login import current_user, AnonymousUserMixin

import logging
import functools
import mariadb

from webapp.utilities import UserPerms
from webapp.utilities.variables import sqldb

from typing import Union


def get_db(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        r = None
        try:
            sqldb.connect()
            r = view(sqldb.cursor, *args, **kwargs)
        except mariadb.Error as e:
            logging.warning(e)
        finally:
            sqldb.close()
        return r
    return wrapper


def perms_required(to_redirect: str, /, *, to_check: Union[list, UserPerms, None]):
    def inner(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            if isinstance(current_user, AnonymousUserMixin):
                return redirect(url_for(to_redirect))
            if isinstance(to_check, list) and current_user.perms in to_check:
                return view(*args, **kwargs)
            if current_user.perms == to_check:
                return view(*args, **kwargs)
            return redirect(url_for(to_redirect))
        return wrapper
    return inner


def police_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if isinstance(current_user, AnonymousUserMixin) or current_user.perms != UserPerms.POLICE:
            if kwargs:
                session['path'] = list(kwargs.values())[0]
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view
