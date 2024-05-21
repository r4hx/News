from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone


class CustomGroup(Group):
    description = models.TextField(
        verbose_name="Описание",
        help_text="Описание группы",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
        help_text="Дата создания этой записи",
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Обновлено",
        help_text="Дата обновления этой записи",
    )

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self) -> str:
        """
        Необходимо для отображение имени в админке
        """
        return str(self.name)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(CustomGroup, self).save(*args, **kwargs)
