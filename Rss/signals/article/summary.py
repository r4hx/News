from django.db.models.signals import post_save
from django.dispatch import receiver

from News.logger import make_logger
from Rss.models import Article
from Rss.tasks import task_summary_text_from_article

logger = make_logger(name="signal-article-summary")


@receiver(post_save, sender=Article)
def signal_summary_text_from_article(sender, instance, created, **kwargs):
    """
    Сигнал для получения пересказа текста статьи
    """
    if created:
        logger.debug(f"Получен сигнал для отправки статьи на самморизацию {instance=}")
        task_summary_text_from_article.apply_async(
            kwargs={"article_id": instance.pk},
        )
