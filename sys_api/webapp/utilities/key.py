from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import codecs

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from typing import Optional


class PrivateKey:
    def __init__(self):
        self.key: Optional[RSAPrivateKey] = None

    def load(self) -> None:
        with open("webapp/private_key.pem", "rb") as key_file:
            self.key = serialization.load_pem_private_key(
                data=key_file.read(),
                password=None,
                backend=default_backend()
            )

    def decrypt(self, message: bytes) -> str:
        original_message = self.key.decrypt(
            codecs.decode(message, 'base64'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')
        return original_message
