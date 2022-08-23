import boto3

from ..config import Config
from ..domain.certificate import Certificate


class AmazonCertificateManager:
    def __init__(self) -> None:
        self.__client = boto3.client("acm")

    def save(self, certificate: Certificate):
        if not Config.get().certificate_arn:
            self.__save_new(certificate)
        else:
            self.__renew_by(certificate)

    def __save_new(self, certificate: Certificate):
        self.__client.import_certificate(
            Certificate=certificate.certificate.encode("utf-8"),
            PrivateKey=certificate.private_key.encode("utf-8"),
            CertificateChain=certificate.fullchain.encode("utf-8"),
            Tags=[
                {
                    "Key": "environment",
                    "Value": Config.get().environemnt.name.lower()
                },
            ]
        )

    def __renew_by(self, certificate: Certificate):
        self.__client.import_certificate(
            CertificateArn=Config.get().certificate_arn,
            Certificate=certificate.certificate.encode("utf-8"),
            PrivateKey=certificate.private_key.encode("utf-8"),
            CertificateChain=certificate.fullchain.encode("utf-8")
        )
