from django.db.models.signals import post_save
from django.dispatch import receiver

from News.logger import make_logger
from Rss.models import Article
from Rss.tasks import task_set_cover_from_article

logger = make_logger(name="signal-cover")


@receiver(post_save, sender=Article)
def signal_set_cover_from_article(sender, instance, created, **kwargs):
    """
    Сигнал для указания обложки статьи
    """
    if created:
        logger.debug(f"Получен сигнал для обложки статьи {instance=}")
        task_set_cover_from_article.apply_async(
            kwargs={"article_id": instance.pk},
        )
