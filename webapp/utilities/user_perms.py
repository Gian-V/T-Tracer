from enum import Enum


class UserPerms(int, Enum):
    ADMIN = 1,
    POLICE = 0
    USER = -1
