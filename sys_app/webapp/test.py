import io

import qrcode


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


qr_loader('ciao')
