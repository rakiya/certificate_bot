from copy import copy
from os import path, rmdir
from typing import List

from certbot import main as certbot
from main.domain.environment import Environment

from ..config import Config
from .certificate import Certificate
from .domains import Domains
from .email_address import EmailAddress


class LetsEncrypt:

    def __init__(self) -> None:
        self.__options = [
            "certonly",
            "-n",
            "--agree-tos",
            "--dns-route53",
            "--config-dir",
            Config.get().working_directory,
            "--work-dir",
            Config.get().working_directory,
            "--logs-dir",
            Config.get().working_directory,
        ]

        if Config.get().environemnt == Environment.PRODUCTION:
            self.__options.extend(
                ["--server", "https://acme-v02.api.letsencrypt.org/directory"]
            )
        else:
            self.__options.append("--staging")

    def issue_certificate(
        self,
        owner: EmailAddress,
        domains: Domains
    ) -> Certificate:
        self.__initialize()

        # certbot を使用して証明書を取得
        options = self.__certbot_options(owner, domains)
        certbot.main(options)

        return Certificate.loads_from(
            path.join(
                Config.get().certificate_directory,
                domains.principal.value
            )
        )

    def __initialize(self):
        if path.exists(Config.get().working_directory):
            rmdir(Config.get().working_directory)

    def __certbot_options(
        self,
        owner: EmailAddress,
        domains: Domains
    ) -> List[str]:
        options = copy(self.__options)

        for domain in domains.to_list():
            options.extend(["-d", f"{domain}"])

        options.extend(["--email", f"{owner}"])

        return options
