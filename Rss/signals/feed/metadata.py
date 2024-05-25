from django.db.models.signals import post_save
from django.dispatch import receiver

from News.logger import make_logger
from Rss.models import Feed
from Rss.tools.rss import get_feed_description_from_url, get_feed_name_from_url

logger = make_logger(name="signal-feed-metadata")


@receiver(post_save, sender=Feed)
def signal_set_rss_metadata(sender, instance, created, **kwargs):
    """
    Сигнал для создания метаданных RSS-ленты
    """
    if created:
        logger.debug(f"Получен сигнал для получения метаданных RSS-ленты {instance=}")
        Feed.objects.filter(pk=instance.pk).update(
            name=get_feed_name_from_url(instance.url),
            description=get_feed_description_from_url(instance.url),
        )
