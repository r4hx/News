class CoverError(Exception):
    """Ошибка при работе с компонентом Cover"""

    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message or self.__doc__, *args, **kwargs)


class CoverStatusCodeError(CoverError):
    """Получена ошибка при запросе изображения компонентом Cover"""
