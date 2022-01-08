from flask_login import UserMixin

from typing import Union


class User(UserMixin):
    def __init__(self, _id: int, mail: str, password: str, perms: Union[int, None]):
        self._id = _id
        self.mail = mail
        self.password = password
        self.perms = perms

    def get_id(self):
        return self.mail

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
