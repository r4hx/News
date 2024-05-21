from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    feeds = models.ManyToManyField(
        "Rss.Feed",
        verbose_name="Источники",
        help_text="Источники, к которым пользователь подписан",
        related_name="users",
        blank=True,
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
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        """
        Необходимо для отображение имени в админке
        """
        return str(self.username)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(CustomUser, self).save(*args, **kwargs)
