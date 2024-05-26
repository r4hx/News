class SummaryError(Exception):
    """Ошибка при работе с компонентом Summary"""

    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message or self.__doc__, *args, **kwargs)


class SummaryServiceResponseError(SummaryError):
    """Получена ошибка при обращении к сервису Summary компонентом Summary"""


class SummaryUrlNotFoundError(SummaryError):
    """Получена ошибка при получении ссылки на статью компонентом Summary"""


class ExtractSummaryError(SummaryError):
    """Получена ошибка при извлечение текста статьи компонентом Summary"""
