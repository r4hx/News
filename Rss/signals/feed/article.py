from django.db.models.signals import post_save
from django.dispatch import receiver

from News.logger import make_logger
from Rss.models import Feed
from Rss.tasks.rss import task_rss_import_from_feeds

logger = make_logger(name="signal-feed-articles-importer")


@receiver(post_save, sender=Feed)
def signal_import_articles_from_rss(sender, instance, created, **kwargs):
    """
    Сигнал для импорта статей из RSS
    """
    if created:
        logger.debug(f"Получен сигнал для импорта статей из RSS {instance=}")
        task_rss_import_from_feeds.apply_async(
            kwargs={"feed_id": instance.pk},
        )
