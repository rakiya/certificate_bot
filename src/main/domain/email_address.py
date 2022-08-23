class EmailAddress:
    def __init__(self, value: str) -> None:
        self.__value = value

    def __str__(self) -> str:
        return self.__value
