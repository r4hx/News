import time
from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


def wait_for_object_to_save_in_store(
    model_class: Type[models.Model],
    pk: int,
    max_attempts: int = 10,
    delay: int = 1,
):
    """
    Ждет сохранения объекта в хранилище.

    Проверяет, сохранен ли объект с заданным primary key в хранилище.
    Если объект не найден, продолжает ожидание в течение определенного количества попыток и с задержкой между ними.

    :param model_class: Класс модели Django.
    :param pk: Primary key объекта.
    :param max_attempts: Максимальное количество попыток.
    :param delay: Задержка между попытками в секундах.
    """
    for _ in range(max_attempts):
        time.sleep(delay)
        try:
            model_class.objects.get(pk=pk)
            return
        except ObjectDoesNotExist:
            continue
    else:
        raise TimeoutError
