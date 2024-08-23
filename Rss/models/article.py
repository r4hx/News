from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from News.settings import APP_SITE_ADDRESS
from Rss.config import ArticleStatusConfigEnum
from Web.tools.idhide import encode_id


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
    related = models.ManyToManyField(
        "Article",
        verbose_name="Похожие записи",
        help_text="Похожие записи",
        blank=True,
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

    def get_encoded_id(self):
        return encode_id(self.id)

    def get_absolute_url(self):
        return f"/{self.source.slug}/{self.get_encoded_id()}/"

    def get_full_url(self):
        url = f"http://{APP_SITE_ADDRESS}/{self.source.slug}/{self.get_encoded_id()}"
        return format_html("<a href={url} target=_blank>{url}</a>", url=url)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Article, self).save(*args, **kwargs)
