from django.db.models.signals import post_save
from django.dispatch import receiver

from News.logger import make_logger
from Rss.config import ArticleStatusConfigEnum
from Rss.models import Article

logger = make_logger(name="signal-article-status")


@receiver(post_save, sender=Article)
def signal_check_ready_to_publish_article(sender, instance, created, **kwargs):
    """
    Сигнал для проверки статуса статьи
    """
    if (
        instance.status is not ArticleStatusConfigEnum.PUBLISHED.value
        and instance.title is not None
        and instance.summary_url is not None
        and instance.summary is not None
        and instance.image_url is not None
    ):
        logger.debug(f"Статья {instance=} готова к публикации")
        Article.objects.filter(pk=instance.pk).update(
            status=ArticleStatusConfigEnum.PUBLISHED.value
        )
