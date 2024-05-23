import os

from django.db import transaction

from News.celery import app
from News.logger import make_logger
from Rss.config import CeleryQueueNameConfigEnum
from Rss.models import Article
from Rss.tools.cover import get_image_from_source_url

logger = make_logger(name="task-cover")

CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
if CELERY_MAX_RETRIES is None:
    raise Exception("CELERY_MAX_RETRIES is not set")

CELERY_COUNTDOWN = os.getenv("CELERY_COUNTDOWN")
if CELERY_COUNTDOWN is None:
    raise Exception("CELERY_COUNTDOWN is not set")


@app.task(
    bind=True,
    queue=CeleryQueueNameConfigEnum.COVER.value,
    max_retries=int(CELERY_MAX_RETRIES),
)
def task_set_cover_from_article(self, article_id: int):
    """
    Задача указания обложки статьи
    """
    logger.debug(f"Создание обложки для статьи {article_id=}")
    try:
        with transaction.atomic():
            try:
                article = Article.objects.select_for_update().get(pk=article_id)
            except Article.DoesNotExist as e:
                logger.exception(f"Статья {article_id=} не существует")
                raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))

            cover = get_image_from_source_url(url=article.url)
            article.image_url = cover
            article.save()
    except Exception as e:
        logger.exception(f"Не удалось создать обложку для статьи {article_id=}")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
