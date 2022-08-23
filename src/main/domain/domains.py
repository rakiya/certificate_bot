from typing import List


class Domain:
    def __init__(self, value: str) -> None:
        self.__value = value

    def __str__(self) -> str:
        return self.__value

    @property
    def value(self) -> str:
        return self.__value


class Domains:
    def __init__(self, values: List[str]) -> None:
        self.__domains = [Domain(value) for value in values]
        self.__principal_domain = min(
            self.__domains,
            key=lambda x: len(x.value)
        )

        for domain in self.__domains:
            if not domain.value.endswith(self.__principal_domain.value):
                raise Exception(f"異なるドメインです: [{', '.join(values)}]")

    @property
    def principal(self) -> Domain:
        return self.__principal_domain

    def join(self, separator: str) -> str:
        return separator.join(self.to_list())

    def to_list(self) -> List[str]:
        return [domain.value for domain in self.__domains]
