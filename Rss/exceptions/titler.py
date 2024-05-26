class TitlerError(Exception):
    """Ошибка при работе с компонентом Titler"""

    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message or self.__doc__, *args, **kwargs)


class GetTitleResponseError(TitlerError):
    """Получена ошибка при получении названия статьи компонентом Titler"""


class TitleNotFoundError(TitlerError):
    """Получена ошибка при получении названия статьи компонентом Titler"""
