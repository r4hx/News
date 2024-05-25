from django.db.models.signals import post_save
from django.dispatch import receiver

from News.logger import make_logger
from Rss.models import Article
from Rss.tasks import task_set_title_from_article

logger = make_logger(name="signal-article-titler")


@receiver(post_save, sender=Article)
def signal_set_article_title(sender, instance, created, **kwargs):
    """
    Сигнал для указания названия статьи
    """
    if created:
        logger.debug(f"Получен сигнал для запроса названия статьи {instance=}")
        task_set_title_from_article.apply_async(
            kwargs={"article_id": instance.pk},
        )
