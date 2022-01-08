from enum import Enum
import mariadb
import bcrypt

from webapp.utilities.decorators import get_db
from webapp.utilities import UserPerms

from typing import Tuple, List, Union, NamedTuple


class UserQuery(str, Enum):
    SELECT_ONE_USER_FROM_TRUCKER = "SELECT * FROM trucker WHERE mail = '{}';"
    SELECT_ONE_USER_FROM_ADMIN = "SELECT * FROM admin WHERE mail = '{}';"
    SELECT_USER_BY_MAIL = "SELECT * FROM {} WHERE mail = '{}';"
    CREATE_TRUCKER = "INSERT INTO trucker(mail, password) VALUES ('{}', '{}');"
    CREATE_ADMIN = "INSERT INTO admin(mail, password, perms) VALUES ('{}', '{}', {});"
    SELECT_ALL_USERS_FROM_TRUCKER = "SELECT * FROM trucker ORDER BY id;"
    SELECT_ALL_USERS_FROM_ADMIN = "SELECT * FROM admin ORDER BY perms DESC;"
    DELETE_USER = "DELETE FROM {} WHERE mail = '{}';"
    SELECT_REQUEST_COUNT_FROM_USER = "SELECT request_count FROM trucker WHERE mail = '{}';"
    INCREMENT_USER_REQUEST_COUNT = "UPDATE trucker SET request_count = {} WHERE mail = '{}';"


def increment_user_request_count(cursor: mariadb.connection.cursor, mail: str) -> None:
    cursor.execute(UserQuery.SELECT_REQUEST_COUNT_FROM_USER.format(mail))
    obj = cursor.fetchone()
    cursor.execute(UserQuery.INCREMENT_USER_REQUEST_COUNT.format(obj.request_count + 1, mail))


def account_existence(cursor: mariadb.connection.cursor, mail: str) -> bool:
    cursor.execute(UserQuery.SELECT_ONE_USER_FROM_TRUCKER.format(mail))
    db_object = cursor.fetchone()
    if not db_object:
        cursor.execute(UserQuery.SELECT_ONE_USER_FROM_ADMIN.format(mail))
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
        mail: str,
        password: str
) -> Tuple[bool, Union[NamedTuple, None]]:
    cursor.execute(UserQuery.SELECT_ONE_USER_FROM_TRUCKER.format(mail))
    db_object = cursor.fetchone()
    if db_object:
        if bcrypt.checkpw(password.encode('utf-8'), db_object.password.encode('utf-8')):
            return True, db_object

    cursor.execute(UserQuery.SELECT_ONE_USER_FROM_ADMIN.format(mail))
    db_object = cursor.fetchone()
    if db_object:
        if bcrypt.checkpw(password.encode('utf-8'), db_object.password.encode('utf-8')):
            return True, db_object

    return False, None


@get_db
def get_user_by_mail(cursor: mariadb.connection.cursor, mail: str) -> NamedTuple:
    cursor.execute(UserQuery.SELECT_USER_BY_MAIL.format('trucker', mail))
    obj = cursor.fetchone()
    if not obj:
        cursor.execute(UserQuery.SELECT_USER_BY_MAIL.format('admin', mail))
        obj = cursor.fetchone()
    return obj


@get_db
def create_account(cursor: mariadb.connection.cursor, mail: str, password: str, perms: int) -> bool:
    if account_existence(cursor, mail):
        return False

    if perms == UserPerms.USER:
        cursor.execute(UserQuery.CREATE_TRUCKER.format(
            mail,
            bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(prefix=b"2a")).decode('utf-8')
        ))
    else:
        cursor.execute(UserQuery.CREATE_ADMIN.format(
            mail,
            bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(prefix=b"2a")).decode('utf-8'),
            perms
        ))
    return True


@get_db
def delete_user(cursor: mariadb.connection.cursor, table: str, mail: str) -> None:
    cursor.execute(UserQuery.DELETE_USER.format(table, mail))
    
    
@get_db
def get_request_count(cursor: mariadb.connection.cursor, mail: str) -> bool:
    cursor.execute(UserQuery.SELECT_REQUEST_COUNT_FROM_USER.format(mail))
    obj = cursor.fetchone()
    if obj.request_count >= 30:
        return False
    return True
