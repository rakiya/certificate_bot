import sys

from .config import Config
from .domain.domains import Domains
from .domain.email_address import EmailAddress
from .domain.lets_encrypt import LetsEncrypt
from .infrastructure.amazon_certificate_manager import AmazonCertificateManager
from .infrastructure.slack_dispatcher import SlackDispatcher

config = Config()
slack_dispatcher = SlackDispatcher(config.slack_url)


def lambda_handler(event, _):
    domains = get_domains(event)
    email_address = get_email_address(event)

    slack_dispatcher.send_good(
        f"Start - {config.environemnt.name}",
        domains.join("\n")
    )

    try:
        # 主処理
        certificate = LetsEncrypt()\
            .issue_certificate(owner=email_address, domains=domains)
        AmazonCertificateManager().save(certificate)
    except Exception:
        _, message, _ = sys.exc_info()
        slack_dispatcher.send_danger("Failure", f"{message}")
        raise

    slack_dispatcher.send_good(
        f"Finish - {config.environemnt.name}",
        domains.join("\n")
    )

    return


def get_domains(event) -> Domains:
    try:
        return Domains(event["domains"])
    except Exception:
        _, message, _ = sys.exc_info()
        slack_dispatcher.send_danger("Failure", f"{message}")
        raise


def get_email_address(event) -> EmailAddress:
    try:
        return EmailAddress(event["email_address"])
    except Exception:
        _, message, _ = sys.exc_info()
        slack_dispatcher.send_danger("Failure", f"{message}")
        raise
