from django.db.models.signals import post_save
from django.dispatch import receiver

from News.logger import make_logger
from Rss.config import ArticleStatusConfigEnum
from Rss.models import Article
from Rss.tasks.related import task_set_related_articles_for_article

logger = make_logger(name="signal-article-publisher")


@receiver(post_save, sender=Article)
def signal_check_ready_to_publish_article(sender, instance, created, **kwargs):
    """
    Сигнал для проверки готовности к публикации статьи.

    Публикует статью, если у неё установлены следующие поля:
    - Название
    - URL пересказа
    - Текст пересказа
    - URL изображения
    """
    if (
        instance.status != ArticleStatusConfigEnum.PUBLISHED.value
        and instance.title is not None
        and instance.summary_url is not None
        and instance.summary is not None
        and instance.image_url is not None
    ):
        logger.debug(f"Получен сигнал для публикации статьи {instance=}")
        instance.status = ArticleStatusConfigEnum.PUBLISHED.value
        instance.save(update_fields=["status"])
        task_set_related_articles_for_article.apply_async(
            kwargs={"article_id": instance.pk}
        )
