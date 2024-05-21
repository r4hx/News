from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from News.settings import CSRF_TRUSTED_ORIGINS


class Feed(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Название источника",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Описание источника",
        blank=True,
        null=True,
    )
    url = models.URLField(
        verbose_name="Ссылка",
        help_text="Ссылка на источник",
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name="slug",
        help_text="slug источника",
        unique=True,
        blank=True,
        null=True,
        editable=False,
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

    def __str__(self):
        return self.name if self.name is not None else str(self.pk)

    @property
    def feed_url(self):
        """
        Возвращает ссылку на RSS канал
        """
        url = CSRF_TRUSTED_ORIGINS[0]
        path = reverse("feed-articles", kwargs={"slug": self.slug})
        return str(url + path)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4())
        self.updated_at = timezone.now()
        super(Feed, self).save(*args, **kwargs)
