from typing import Union

from flask import (
    redirect, url_for, session
)
from flask_login import current_user, AnonymousUserMixin
import functools
import logging
import mariadb

from webapp.utilities.user_perms import UserPerms
from webapp.utilities.variables import sqldb


def get_db(func):
    def wrapper(*args, **kwargs):
        r = None
        try:
            sqldb.connect()
            r = func(sqldb.cursor, *args, **kwargs)
        except mariadb.Error as e:
            logging.warning(e)
        finally:
            sqldb.close()
        return r
    return wrapper


def join_required(to_redirect: str, /, *, to_check: Union[UserPerms, None]):
    def inner(view):
        def wrapper(*args, **kwargs):
            if isinstance(current_user, AnonymousUserMixin) or current_user.perms != to_check:
                return redirect(url_for(to_redirect))
            return view(*args, **kwargs)
        return wrapper
    return inner


def police_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if isinstance(current_user, AnonymousUserMixin) or getattr(current_user.user, 'perms', None) != 0:
            if kwargs:
                session['path'] = list(kwargs.values())[0]
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
