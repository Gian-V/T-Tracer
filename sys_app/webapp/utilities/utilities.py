from collections import namedtuple
import io
import qrcode

from typing import List


Marks = namedtuple('Marks', ['date', 'location'])


def generate_geo_list(raw_str: str) -> List[Marks]:
    return [
        Marks(" ".join(obj[0].split("_")), (float(obj[1]), float(obj[2])))
        for i in raw_str.split('|')[:-1]
        if (obj := i.split(' ')) and True
    ]


def verify_form(*args, **kwargs) -> bool:
    for field in (args + tuple(kwargs.items())):
        if isinstance(field, str) and not field:
            return False
    return True


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
