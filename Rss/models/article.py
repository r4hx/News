from django.db import models
from django.utils import timezone

from Rss.config import ArticleStatusConfigEnum


class Article(models.Model):
    source = models.ForeignKey(
        "Feed",
        on_delete=models.CASCADE,
        verbose_name="Источник",
        help_text="Источник статьи",
    )
    url = models.URLField(
        verbose_name="Ссылка",
        help_text="Ссылка на статью",
    )
    title = models.TextField(
        verbose_name="Заголовок",
        help_text="Заголовок статьи",
        blank=True,
        null=True,
    )
    summary_url = models.URLField(
        verbose_name="Ссылка на пересказ",
        help_text="Ссылка на пересказ статьи",
        blank=True,
        null=True,
    )
    summary = models.TextField(
        verbose_name="Пересказ",
        help_text="Пересказ статьи",
        blank=True,
        null=True,
    )
    image_url = models.URLField(
        verbose_name="Ссылка на изображение",
        help_text="Ссылка на изображение статьи",
        blank=True,
        null=True,
    )
    status = models.IntegerField(
        choices=[(status.value, status.name) for status in ArticleStatusConfigEnum],
        verbose_name="Статус",
        help_text="Статус статьи",
        default=0,
    )
    retry_count = models.IntegerField(
        default=0,
        verbose_name="Количество попыток обработки статьи",
        help_text="Количество попыток обработки статьи",
    )
    error_text = models.TextField(
        verbose_name="Текст ошибки",
        help_text="Текст ошибки при обработке статьи",
        blank=True,
        null=True,
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
        unique_together = ("source", "url")

    def __str__(self):
        return self.title if self.title is not None else str(self.url)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Article, self).save(*args, **kwargs)
