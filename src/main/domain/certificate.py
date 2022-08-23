from __future__ import annotations
from os import path


class Certificate:

    def __init__(
        self,
        certificate: str,
        private_key: str,
        fullchain: str
    ) -> None:
        self.__certificate = certificate
        self.__private_key = private_key
        self.__fullchain = fullchain

    @classmethod
    def loads_from(cls, directory: str) -> Certificate:
        with open(path.join(directory, "cert.pem"), mode='r', encoding="utf-8") as f:
            certificate = f.read()
        with open(path.join(directory, "privkey.pem"), mode='r', encoding="utf-8") as f:
            private_key = f.read()
        with open(path.join(directory, "fullchain.pem"), mode='r', encoding="utf-8") as f:
            fullchain = f.read()

        return Certificate(certificate, private_key, fullchain)

    @property
    def certificate(self) -> str:
        return self.__certificate

    @property
    def private_key(self) -> str:
        return self.__private_key

    @property
    def fullchain(self) -> str:
        return self.__fullchain
