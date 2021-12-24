import re
from typing import Tuple

MAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def verify_form(*args, **kwargs) -> bool:
    for field in (args + tuple(kwargs.items())):
        if isinstance(field, str):
            if not field or (6 > len(field) > 16):
                return False
    return True


def send_document(car_id: str, to_start: str, to_arrive: str, email: str) -> Tuple[bool, str]:
    print(re.search(MAIL_REGEX, email))
    if not verify_form(car_id, to_start, to_arrive, email) or re.search(MAIL_REGEX, email) is None:
        return False, "You missed some fields"
    return True, "Request sent correctly!"
