from __future__ import annotations

from os import environ

from .domain.environment import Environment


class Config:

    __instance = None

    def __init__(self) -> None:
        self.__environment = \
            Environment[environ["ENVIRONMENT"].upper()] or Environment.DEVELOPMENT
        self.__slack_url = environ["CERTIFICATE_BOT_SLACK_URL"]
        self.__certificate_arn = environ.get("CERTIFICATE_ARN", None)
        self.__working_directory = "/tmp/certificate_bot"

    @classmethod
    def get(cls) -> Config:
        if cls.__instance is None:
            cls.__instance = Config()

        return Config()

    @property
    def environemnt(self) -> Environment:
        return self.__environment

    @property
    def slack_url(self) -> str:
        return self.__slack_url

    @property
    def certificate_arn(self) -> str:
        return self.__certificate_arn

    @property
    def working_directory(self) -> str:
        return self.__working_directory

    @property
    def certificate_directory(self) -> str:
        return f"{self.__working_directory}/live"
