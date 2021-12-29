from enum import Enum
import mariadb
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.utilities.decorators import get_db
from webapp.utilities.user_perms import UserPerms

from typing import Tuple, List, Union, NamedTuple


class UserQuery(str, Enum):
    SELECT_ONE_USER_FROM_TRUCKER = "SELECT * FROM trucker WHERE username = '{}';"
    SELECT_ONE_USER_FROM_ADMIN = "SELECT * FROM admin WHERE username = '{}';"
    SELECT_USER_BY_USERNAME = "SELECT * FROM {} WHERE username = '{}';"
    CREATE_TRUCKER = "INSERT INTO trucker(username, password) VALUES ('{}', '{}');"
    CREATE_ADMIN = "INSERT INTO admin(username, password, perms) VALUES ('{}', '{}', {});"
    SELECT_ALL_USERS_FROM_TRUCKER = "SELECT * FROM trucker ORDER BY id;"
    SELECT_ALL_USERS_FROM_ADMIN = "SELECT * FROM admin ORDER BY perms;"
    DELETE_USER = "DELETE FROM {} WHERE username = '{}';"


def account_existence(cursor: mariadb.connection.cursor, username: str) -> bool:
    cursor.execute(UserQuery.SELECT_ONE_USER_FROM_TRUCKER.format(username))
    db_object = cursor.fetchone()
    if not db_object:
        cursor.execute(UserQuery.SELECT_ONE_USER_FROM_ADMIN.format(username))
        db_object = cursor.fetchone()
        if not db_object:
            return False
    return True


@get_db
def get_all_users(cursor: mariadb.connection.cursor) -> List[NamedTuple]:
    cursor.execute(UserQuery.SELECT_ALL_USERS_FROM_TRUCKER)
    trucker_list = cursor.fetchall()
    cursor.execute(UserQuery.SELECT_ALL_USERS_FROM_ADMIN)
    admin_list = cursor.fetchall()
    admin_list.extend(trucker_list)
    return admin_list


@get_db
def check_user_login(
        cursor: mariadb.connection.cursor,
        username: str,
        password: str
) -> Tuple[bool, Union[NamedTuple, None]]:
    cursor.execute(UserQuery.SELECT_ONE_USER_FROM_TRUCKER.format(username))
    db_object = cursor.fetchone()
    if db_object:
        if check_password_hash(db_object.password, password):
            return True, db_object

    cursor.execute(UserQuery.SELECT_ONE_USER_FROM_ADMIN.format(username))
    db_object = cursor.fetchone()
    if db_object:
        if check_password_hash(db_object.password, password):
            return True, db_object

    return False, None


@get_db
def get_user_by_username(cursor: mariadb.connection.cursor, username: str) -> NamedTuple:
    cursor.execute(UserQuery.SELECT_USER_BY_USERNAME.format('trucker', username))
    obj = cursor.fetchone()
    if not obj:
        cursor.execute(UserQuery.SELECT_USER_BY_USERNAME.format('admin', username))
        obj = cursor.fetchone()
    return obj


@get_db
def create_account(cursor: mariadb.connection.cursor, username: str, password: str, perms: int) -> bool:
    if account_existence(cursor, username):
        return False

    if perms == UserPerms.USER:
        cursor.execute(UserQuery.CREATE_TRUCKER.format(username, generate_password_hash(password)))
    else:
        cursor.execute(UserQuery.CREATE_ADMIN.format(username, generate_password_hash(password), perms))
    return True


@get_db
def delete_user(cursor: mariadb.connection.cursor, table: str, username: str) -> None:
    cursor.execute(UserQuery.DELETE_USER.format(table, username))
