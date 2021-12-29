import re
import qrcode
import io

from typing import Tuple

MAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def verify_form(*args, **kwargs) -> bool:
    for field in (args + tuple(kwargs.items())):
        if isinstance(field, str):
            if not field:
                return False
    return True


def validate_form(car_id: str, to_start: str, to_arrive: str, email: str) -> Tuple[bool, str]:
    print(re.search(MAIL_REGEX, email))
    if not verify_form(car_id, to_start, to_arrive, email) or re.search(MAIL_REGEX, email) is None:
        return False, "You missed some fields"
    return True, "Request sent correctly!"


def qr_loader(data: str) -> bytes:
    qr = qrcode.QRCode(
        version=1,
        box_size=20,
        border=10
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    in_mem_file = io.BytesIO()
    img.save(in_mem_file, format="PNG")
    # reset file pointer to start
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    return img_bytes
